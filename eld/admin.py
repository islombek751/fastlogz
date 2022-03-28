from . import models
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.contrib.auth.models import Group
from .forms import UserChangeForm, UserCreationForm, CompanyAdminForm, DriverAdminForm


class UserAdmin(BaseUserAdmin):
    def image_tag(self, obj):
        try:
            return format_html(
                f'<a href="{obj.image.url}" class="change-form">'
                f'<img class="baton-image-preview" src="{obj.image.url}"/>'
                '</div>')
        except ValueError:
            return format_html("none")
    image_tag.short_description = "Image"
    image_tag.allow_tags = True
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'image_tag')
    list_filter = ('groups', )
    readonly_fields = ('image_tag', )
    fieldsets = (
        (None, {'fields': (tuple(['email', ]), 'password', 'image')}),
        ('Contact information', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'groups', 'password1', 'password2', 'notificationToUser'),
        }),
    )
    search_fields = ('email', 'first_name', "last_name",)
    ordering = ('email',)
    filter_horizontal = ()


class CompanyAdmin(admin.ModelAdmin):
    form = CompanyAdminForm
    exclude = [
        'image'
    ]
    add_form = CompanyAdminForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password', ),
        }),
    )

    def save_model(self, request, obj, form, change):
        data = form.cleaned_data
        user = get_user_model().objects.create(email=data.get('email', None))
        user.set_password(data.get('password', None))
        user.save()

        obj.image = user
        super(CompanyAdmin, self).save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        list_deleting_users = list(queryset.values_list('email', flat=True))
        get_user_model().objects.filter(email__in=list_deleting_users).delete()
        super(CompanyAdmin, self).delete_model(request, queryset)


class DriversAdmin(admin.ModelAdmin):
    form = DriverAdminForm
    exclude = ['image']

    def save_model(self, request, obj, form, change):
        data = form.cleaned_data
        if not get_user_model().objects.filter(email=data.get('email', None)).exists():
            user = get_user_model().objects.create(email=data.get('email', None))
            group = Group.objects.get(name='Driver')
            user.groups.add(group)
            user.set_password(data.get('password', None))
            user.save()
            super(DriversAdmin, self).save_model(request, obj, form, change)
        else:
            super(DriversAdmin, self).save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        list_deleting_users = list(queryset.values_list('email', flat=True))
        get_user_model().objects.filter(email__in=list_deleting_users).delete()
        super(DriversAdmin, self).delete_model(request, queryset)


admin.site.register(get_user_model(), UserAdmin)
admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.ELD)
admin.site.register(models.Trailer)

admin.site.register(models.Vehicle)
admin.site.register(models.DRIVERS, DriversAdmin)


admin.site.site_header = "FastLogs"
