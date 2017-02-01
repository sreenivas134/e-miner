from django.shortcuts import render
from django.db.models import Q
from eminer.models import NewEntry, Tag
from eminer.forms import EntryForm, TagForm, EditPostForm, PublishForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_deny, xframe_options_sameorigin
# Create your views here.


def BlogView(request, post_name=None, count=1, tag=None):
    recent = NewEntry.objects.filter(published=True).order_by('-modified')[:10]
    user_ip = request.META.get('REMOTE_ADDR')
    if post_name:
        posts = NewEntry.objects.filter(slug=post_name)
    elif tag:
        tags = Tag.objects.get(slug=tag)
        posts = NewEntry.objects.filter(Q(tag = tags) & Q(published = True))
    else:
        count = int(count)
        posts = NewEntry.objects.filter(published=True).order_by('-modified')[count-1:count]
    return render(request, 'eminer/index.html', {'posts':posts, 'count':count, 'recent':recent, 'user_ip':user_ip})

def About(request):
    recent = NewEntry.objects.filter(published=True).order_by('-modified')[:10]
    return render(request, 'eminer/about.html', {'recent':recent})


# Add posts
@xframe_options_deny
@login_required
def AddPost(request, post_name_edit=None):
    not_published = NewEntry.objects.filter(published = False).order_by('-modified')
    recent = NewEntry.objects.filter(published=True).order_by('-modified')[:10]
    if post_name_edit:
        if request.method == 'POST':
            record = NewEntry.objects.get(slug = post_name_edit)
            form = EditPostForm(request.POST, instance=record)
            if form.is_valid():
                post = form.save(commit = False)
                post.save()
                form.save_m2m()
                return HttpResponseRedirect('/publisherview/')
        else:
            record = NewEntry.objects.get(slug = post_name_edit)
            form = EditPostForm(instance = record)
            #not_published.pop(record)
            return render(request, 'eminer/edit_post.html',{'form':form, 'not_published':not_published,'recent':recent})

    else:
        if request.method == 'POST':
            form = EntryForm(request.POST)
            if form.is_valid():
                post = form.save(commit = False)
                post.save()
                form.save_m2m()
                return BlogView(request)
            else:
                print form.errors
        else:
            form = EntryForm()
        return render(request, 'eminer/add_post.html',{'form':form, 'not_published':not_published,'recent':recent})




# Add tag
@login_required
def AddTag(request):
    recent = NewEntry.objects.filter(published=True).order_by('-modified')[:10]
    if request.method == 'POST':
        form = TagForm(request.POST)

        if form.is_valid():
            post = form.save(commit = True)
            post.save()
            return AddPost(request)
        else:
            print form.errors

    else:
        form = TagForm()

    return render(request, 'eminer/add_tag.html',{'form':form,'recent':recent})




#Author View of the Models
@xframe_options_deny
@user_passes_test(lambda u: u.is_staff)
def PublisherView(request, post_name_edit=None):
    not_published = NewEntry.objects.filter(published = False).order_by('-modified')
    published_posts = NewEntry.objects.filter(published = True).order_by('-modified')[:10]
    recent = NewEntry.objects.filter(published=True).order_by('-modified')[:10]

    return render(request, 'eminer/admin_view.html', {'not_published':not_published, 'published_posts':published_posts, 'recent':recent})

@xframe_options_deny
@user_passes_test(lambda u: u.is_staff)
def PublishView(request, post_name=None):
    recent = NewEntry.objects.filter(published=True).order_by('-modified')[:10]
    if post_name:
        if request.method == 'POST':
            item = NewEntry.objects.get(slug = post_name)
            form = PublishForm(request.POST, instance = item)
            if form.is_valid():
                post = form.save(commit = True)
                post.save()
                return HttpResponseRedirect('/publisherview/')
        else:
            item = NewEntry.objects.get(slug = post_name)
            form = PublishForm(instance = item)

        return render(request, 'eminer/publish.html', {'form':form, 'post':item,'recent':recent,})
