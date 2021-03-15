def project_count(request):
   return { 'total_project' : ProjectInfo.objects.all().count() }
