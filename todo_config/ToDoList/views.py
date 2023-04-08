from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_bytes  
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.views.generic import *
from django.conf import settings
from django.http import Http404
from django.db.models import Q

from .forms import *
from .models import Task, UserToken




class Index(TemplateView):
    #info page
    template_name = 'ToDoList/main_page.html' 


class UserRegister(FormView):
    form_class = RegisterForm
    template_name = 'ToDoList/auth_form.html'

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            if not User.objects.filter(email=email).exists():
                new_user = User.objects.create_user(username=username, password=password,
                                                    email=email, is_active=False
                                                    )
                messages.success(request, 
                        f'Check {email} the registration link will expire after one hour.'
                        )

                token = UserToken.get_or_create_token(user=new_user)
                uidb = urlsafe_base64_encode(force_bytes(new_user.pk))

                link = f"http://{request.get_host()}/activation/{uidb}/{token.token}"
                send_mail(
                    'TO-DO-LIST - verification',
                    f'Click on the link to complete the registration - {link}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=True,
                )
                return redirect('login')
            else:
                form.add_error('email', 'This email is already get') 
        return render(request, 'ToDoList/auth_form.html', {'form': form, 'title':'Register'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context


class UserVerification(View):

    def get(self, request, uidb64, token):
        try:
            user_pk = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=user_pk)
        except (TypeError, ValueError, 
                OverflowError, user.DoesNotExist):
            user = None
        
        if user is not None:
            try:
                user_token = UserToken.objects.get(user=user, token=token)
            except UserToken.DoesNotExist:
                raise Http404('Token is not valid')

            if not user_token.is_expired():
                user.is_active = True
                user.save()
                login(request, user=user)
                messages.info(request, 'Registration is complete')
                user_token.delete()
                return redirect('task_list')

            user_token.delete()

            raise Http404('Token is expired')
        raise Http404()



class UserLogin(FormView):
    form_class = LoginForm
    template_name = 'ToDoList/auth_form.html'

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username,
                                         password= password,
                                         )
            if user is not None:
                login(request, user=user)
                return redirect('task_list')
        form.add_error('__all__', 'Enter the correct data')
        return render(request, 'ToDoList/auth_form.html', {'form':form, 'title':'Login'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


class UserLogout(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect('login')


class TaskList(LoginRequiredMixin, ListView):
    model = Task

    context_object_name = 'tasks'
    template_name = 'ToDoList/task_list.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('complete', '-updated_at')


class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm

    template_name = 'ToDoList/task_form.html'
    
    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=True)
            new_task.user = self.request.user
            new_task.save()
            messages.success(request, 'Task created')
            return redirect('task_list')
        return render(request, 'ToDoList/task_form.html', {'form':form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context


class TaskDetails(LoginRequiredMixin, DetailView): 
    model = Task
    template_name = 'ToDoList/task_details.html'

    def get_queryset(self):
        try:
            return Task.objects.filter(user=self.request.user)
        except Task.DoesNotExist:
            raise Http404("Task not found")


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task

    def get(self, request, pk):
        try:
            task = Task.objects.get(user=self.request.user, pk=pk)
        except Task.DoesNotExist:
            raise Http404("Task not found")
        
        task.delete()
        return redirect('task_list')


class EditTask(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm

    template_name = 'ToDoList/task_form.html'

    def get_queryset(self):
        try:
            return Task.objects.filter(user=self.request.user)
        except Task.DoesNotExist:
            raise Http404("Task not found")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

class Searched(LoginRequiredMixin, View):

    def post(self, request):
        context = {}
        if request.method == 'POST' and request.POST['searched'] != '':
            data = str(request.POST['searched'])
            if len(data) >= 30:
                data = data[:35] + '...'
            tasks = Task.objects.filter(user=request.user).filter(
                                        Q(title__icontains=data) | 
                                        Q(description__icontains=data)
                                        )
            context['searched'] = data
            context['tasks'] = tasks
        return render(request, 'ToDoList/searched.html', context)


class ForgotPassword(FormView):
    form_class = EmailForm
    template_name = 'ToDoList/auth_form.html'

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = UserToken.get_or_create_token(user=user)
                uidb = urlsafe_base64_encode(force_bytes(user.pk))
                link = f'http://{request.get_host()}/reset-password/{uidb}/{token.token}/'

                send_mail(
                    'TO-DO-LIST new password',
                    f'''
                            Click on the link to reset password - {link}
                            if this is not you then ignore this letter
                    ''',
                    settings.EMAIL_HOST_USER,
                    [email,],
                    fail_silently=True
                    )
                messages.info(request, 'Check your email for verification')

            else:
                form.add_error('email', 'Account with this email not found')
        return render(request, 'ToDoList/auth_form.html', 
                            {'form':form,
                             'title':'Confirm'
                             }
                    )
                    

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = 'Confirm'
        return context



class ResetPassword(View):

    def get(self, request, uidb, token):
        user_pk = urlsafe_base64_decode(uidb)
        try:
            user = User.objects.get(pk=user_pk)
        except ObjectDoesNotExist:
            raise Http404()
        if user.usertoken.token == token and not user.usertoken.is_expired:
            return render(request, 'ToDoList/auth_form.html', 
                            {'form':NewPasswordForm(user=user), 
                             'title':'Reset password', 
                            }
                        )
        else:
            raise Http404('Token is expired')
        
    def post(self, request, uidb, token):
        user_pk = urlsafe_base64_decode(uidb)
        try:
            user = User.objects.get(pk=user_pk)
        except ObjectDoesNotExist:
            raise Http404()

        form = NewPasswordForm(data=request.POST, user=user)
        if form.is_valid():
            form.save()
            user.save()
            return redirect('login')
        return render(request, 'ToDoList/auth_form.html',
                        {'form':form, 
                         'title':'Reset password', 
                        }
                    )
