import os
from django.shortcuts import render
from django.contrib import messages
from django.http import Http404
from properties.classes.ConnectorProperties import ConnectorProperties
from properties.forms import ContactForm
from properties.classes.ConnectorContactRequest import ConnectorContactRequest

connector = ConnectorProperties(os.environ.get('API_KEY',))
connector_contact_request = ConnectorContactRequest(os.environ.get('API_KEY',))

def index(request, page = 1):

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

    # get a form deppending on the request method
    form = process_contact_request(request, id)

    # get the property
    response = connector.get_property(id)

    # verify if the property exists
    if response.status_code != 200:
        raise Http404
    property = response.json()

    # verify if the property has images
    if len(property['property_images']) > 0:
        property_image = property['property_images'][0]['url']
    else:
        property_image = ''

    context = {
        'property': property,
        'property_image': property_image,
        'form': form
    }

    return render(request, 'show_property.html', context)

def process_contact_request(request, id):

    # if the request is a POST, we need to process the form data and send the contact request
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            response = connector_contact_request.post_contact_request(
                name = name,
                phone = phone,
                email = email,
                message = message,
                property_id = id,
                source = 'myprops.com'
            )

            # set a message even if is successful or not
            # if is successful, clean up the form
            if response.status_code == 200:
                messages.success(request, 'Tu solicitud ha sido enviada')
                form = ContactForm()
            else:
                messages.error(request, response.json()['error'])
        else:
            # if the form is not valid, set a message and return the form and its data
            messages.error(request, 'Algunos datos no son válidos')
    else:
        form = ContactForm()

    # return an clean form if the request is get or succesful post
    return form

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)