from django.shortcuts import render_to_response
from django.template import RequestContext
from hellokitty.apps.torrentkitty.models import Resources

# Create your views here.


def home(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))


def export(request):
    resources = Resources.objects.filter(status=False)
    resources.update(status=True)
    return render_to_response('results.html',
                              {'resources': resources},
                              context_instance=RequestContext(request))
