from django.contrib import admin
from teams import models
from django.http import HttpResponse
import xlwt

#def export_xls(modeladmin, request, queryset):
#    response = HttpResponse(content_type='application/ms-excel')
#    response['Content-Disposition'] = 'attachment; filename=models.Team.xls'
#    wb = xlwt.Workbook(encoding='utf-8')
#    ws = wb.add_sheet('Team')
#
#    row_num = 0
#
#    columns = [
#        ('Team_id', 1000),
#        ('TeamName', 6000),
#        ('Group', 5000),
#        ('MemberName', 5000),
#        ('MemberID', 5000),
#        ('Is_leader?', 5000),
#        ('first_time', 5000),
#    ]

#    font_style = xlwt.XFStyle()
#    font_style.font.bold = True

#    for col_num in range(len(columns)):
#        ws.write(row_num, col_num, columns[col_num][0], font_style)
#        ws.col(col_num).width = columns[col_num][1]

#    font_style = xlwt.XFStyle()
#    font_style.alignment.warp = 1
#    obj_num = 0

#    for obj in queryset:
#        row_num += 1
#        obj_num += 1
#        row1 = [
#            obj_num,
#            obj.name,
#            obj.get_group_display(),
#            obj.leader.username,
#            obj.leader.profile.student_id,
#            'Yes',
#            obj.get_pre_time_display(),
#        ]
#        for col_num in range(len(row1)):
#            ws.write(row_num, col_num, row1[col_num], font_style)

#        for member in obj.members.all():
#            row_num += 1
#            row = [
#                member.username,
#                member.profile.student_id,
#                'No',
#            ]
#            for col_num in range(len(row)):
#                ws.write(row_num, col_num+3, row[col_num], font_style)

#    wb.save(response)
#    return response


#export_xls.short_description = u"Export XLS"
class TeamAdmin(admin.ModelAdmin):
    model = models.Team
    filter_horizontal = ('members', )
 #   actions = [export_xls, ]



admin.site.register(models.Team, TeamAdmin)
