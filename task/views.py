import csv
import io
from itertools import islice

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, RedirectView, FormView, CreateView, DeleteView, UpdateView, TemplateView
from django.views import View
from django.utils.translation import gettext as _

from config._ajax import AjaxResponseMixin
from task.forms import TodoForm, LoginForm
from task.models import Todo

__all__ = ('LogoutView', 'UserLoginView', 'HomePageRedirectView', 'TodoListView', 'TodoCreateView', 'TodoDeleteView',
           'TodoUpdateView', 'TodoExportView', 'TodoImportView')


class LogoutView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('login')

    def get(self, request, **kwargs):
        logout(request)

        if request.GET.get('next'):
            self.url = '{}?next={}'.format(self.url, request.GET.get('next'))

        return super(LogoutView, self).get(request, **kwargs)


class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('task:todo_list'))

        return super(UserLoginView, self).get(request, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        profile = User.objects.filter(email=email)

        if not profile:
            messages.error(self.request, _('User not found'))
            return self.form_invalid(form)

        profile = profile[0]
        if not profile.is_active:
            messages.error(self.request, _('User status is not active'))
            return self.form_invalid(form)

        user = authenticate(username=profile.username, password=password)

        if not user:
            messages.error(self.request, _('Wrong password'))
            return self.form_invalid(form)

        login(self.request, user)

        if self.request.GET.get('next'):
            url = self.request.GET.get('next')
        else:
            url = reverse('task:todo_list')

        return redirect(url)


class HomePageRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse('task:todo_list')
        return reverse('login')


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    paginate_by = 4
    form_class = TodoForm
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TodoListView, self).get_context_data(**kwargs)
        context['form'] = self.form_class
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['text']

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user_id = self.request.user.id
        task.save()
        messages.success(self.request, _(u'Todo created'))
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('task:todo_list')


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo

    def get_object(self, queryset=None):
        _id = self.kwargs.get('id')
        return get_object_or_404(self.model, id=_id, user_id=self.request.user.id)

    def get_success_url(self):
        return reverse('task:todo_list')

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        success_url = self.get_success_url()
        object.delete()
        messages.success(self.request, _(u'Todo deleted'))
        return redirect(success_url)


class TodoUpdateView(LoginRequiredMixin, AjaxResponseMixin, UpdateView):
    model = Todo

    def get_object(self, queryset=None):
        _id = self.kwargs.get('id')
        return get_object_or_404(self.model, id=_id, user_id=self.request.user.id)

    def get_ajax(self, request, *args, **kwargs):
        object = self.get_object()
        if '/complete/' in request.path:
            object.is_completed = True
        elif '/uncomplete/' in request.path:
            object.is_completed = False
        object.save(update_fields=['is_completed', 'last_updated'])
        return render(request, 'task/todo_list_single_row.html', {'object': object})


class TodoExportView(LoginRequiredMixin, View):
    queryset = Todo.objects.all()

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="todo_list.csv"'

        writer = csv.writer(response)
        writer.writerow(['User', 'Todo', 'Status', 'Created', 'Updated'])
        for obj in self.queryset.iterator():
            status = 'Completed' if obj.is_completed else 'Not Completed'
            writer.writerow([obj.get_user_full_name, obj.text, status,
                             obj.created_time.astimezone().strftime("%d-%m-%Y %H:%M:%S"),
                             obj.last_updated.astimezone().strftime("%d-%m-%Y %H:%M:%S")])

        return response


class TodoImportView(LoginRequiredMixin, View):
    model = Todo
    success_url = reverse_lazy('task:todo_list')

    def bulk_create(self, objs):
        while True:
            batch = list(islice(objs, 100))
            if not batch:
                break
            self.model.objects.bulk_create(batch)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('csv_file')
        if not csv_file.content_type == 'text/csv':
            messages.error(request, _(u'Format error!'))
            return redirect(self.success_url)
        dataset = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(dataset)
        next(io_string)

        objs = []
        for row in csv.reader(io_string, delimiter=','):
            status = True if row[1] == 'Completed' else False
            objs.append(self.model(user_id=request.user.id, text=row[0], is_completed=status))
        self.bulk_create(iter(objs))
        messages.success(request, 'Todo created')

        return redirect(self.success_url)


class UserStatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'task/user_statistics.html'

    def get_context_data(self, **kwargs):
        context = super(UserStatisticsView, self).get_context_data(**kwargs)
        counts = Todo.objects.filter(user_id=self.request.user.id).aggregate(
            completed_count=Count('id', filter=Q(is_completed=True)),
            not_completed_count=Count('id', filter=Q(is_completed=False))
        )
        context['objs_count_list'] = counts
        completed_percentage = int((100 * counts['completed_count']) / (counts['completed_count'] + counts['not_completed_count']))
        context['percentages_list'] = [completed_percentage, 100 - completed_percentage]
        return context

