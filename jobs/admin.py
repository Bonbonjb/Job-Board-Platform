from django.contrib import admin
from .models import Job, Category
from applications.models import Application

class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    readonly_fields = ['user', 'cover_letter', 'resume', 'created_at']
    can_delete = False

# Inline for Jobs under Category
class JobInline(admin.TabularInline):
    model = Job
    extra = 1  # number of empty job forms shown

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'date_posted', 'is_active')
    list_filter = ('category', 'location', 'is_active', 'date_posted')
    search_fields = ('title', 'company', 'location', 'description')
    ordering = ['-date_posted']
    inlines = [ApplicationInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    inlines = [JobInline]

admin.site.unregister(Category)  # in case it was already registered
admin.site.register(Category, CategoryAdmin)