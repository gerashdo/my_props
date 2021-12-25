from django.shortcuts import render
from properties.classes.ConnectorProperties import ConnectorProperties

def index(request, page = 1):

    connector = ConnectorProperties('l7u502p8v46ba3ppgvj5y2aad50lb9')
    response = connector.get_properties_page(page = page, limit = 15, statuses = ['published'])
    properties = response.json()['content']
    nextPage = response.json()['pagination']['next_page']

    context = {
        'properties': properties,
        'next_page': nextPage,
        'page': page + 1
    }

    return render(request, 'index.html', context)

def show_property(request, id):

    # connector = ConnectorProperties('l7u502p8v46ba3ppgvj5y2aad50lb9')
    # response = connector.get_property(id)
    # property = response.json()

    # context = {
    #     'property': property
    # }

    return render(request, 'show_property.html')
