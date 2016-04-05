from django.contrib import admin
from . import models


# Register your models here.
class ModelsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'resolution')
    list_per_page = 100
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = False


admin.site.register(models.Model, ModelsAdmin)


class PackagesAdmin(admin.ModelAdmin):
    list_display = ('cid', 'mod', 'description', 'status', 'pincode', 'md5',
                    'size', 'type', 'created', 'dirty', 'share', 'completed',
                    'target', 'targetcode')
    list_per_page = 100
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = False


admin.site.register(models.Packages, PackagesAdmin)


class RawfilesAdmin(admin.ModelAdmin):
    list_display = ('pb_type', 'pb_info', 'pac', 'name', 'download_url',
                    'suffix', 'modified', 'crop', 'processed_url')
    list_per_page = 100
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = False


admin.site.register(models.Rawfiles, RawfilesAdmin)


class PrebuiltInfoAdmin(admin.ModelAdmin):
    #list_display = ('id','res_name','res_author','res_desp', 'res_length',  'res_file_path','res_download_num', 'res_recommend_level',  'create_time','last_modify_time', 'res_category','res_type','extra_info')
    list_display = ('id', 'res_name', 'res_author', 'res_file_path',
                    'create_time', 'res_category', 'res_type')
    search_fields = ('res_name', 'res_author')
    list_filter = ('res_category', 'res_type')
    fields = ('res_name', 'res_author', 'res_file_path', 'res_category',
              'res_type', 'res_desp', 'res_recommend_level', 'extra_info')
    list_per_page = 100
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = False


admin.site.register(models.PbInfo, PrebuiltInfoAdmin)


class PrebuiltCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'type_id')
    list_per_page = 100
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = False


admin.site.register(models.PbCategory, PrebuiltCategoryAdmin)


class PrebuiltTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')
    list_per_page = 100
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = False


admin.site.register(models.PbType, PrebuiltTypeAdmin)


class HelpQAAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'modified')
    fields = ('question', 'answer')
    list_per_page = 100
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = False


admin.site.register(models.HelpQA, HelpQAAdmin)
