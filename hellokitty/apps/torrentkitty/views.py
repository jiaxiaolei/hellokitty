from django.shortcuts import render_to_response
from django.template import RequestContext
from hellokitty.apps.torrentkitty.models import Resources
import copy

# Create your views here.


def home(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))


def export(request):
    resources = Resources.objects.filter(status=False)
    results = copy.deepcopy(resources)
    # resources.update(status=True)
    return render_to_response('results.html',
                              {'resources': results},
                              context_instance=RequestContext(request))
