from django.shortcuts import render
from django.http import HttpResponse
from django import forms


class newProblemForm(forms.Form):
    UserID = forms.CharField(label='User ID')
    problemDescription = forms.CharField(
        label='Problem Description', widget=forms.Textarea, max_length=300)
    deviceSerialNumber = forms.CharField(
        label='Device Serial Number', max_length=64)

    CHOICES = [('on', 'on'),
               ('off', 'off'),
               ('blinking', 'blinking')]

    statusIndicatorLights1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect,
                                               label='Status Indicator Lights 1')
    statusIndicatorLights2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect,
                                               label='Status Indicator Lights 2')
    statusIndicatorLights3 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect,
                                               label='Status Indicator Lights 3')


def addProblem(request):
    theResponse = ""
    if request.method == "POST":
        form = newProblemForm(request.POST)

        if form.is_valid():
            serial = form.cleaned_data["deviceSerialNumber"]
            #### start logic ###
            statusIndicatorLights1 = form.cleaned_data["statusIndicatorLights1"]
            statusIndicatorLights2 = form.cleaned_data["statusIndicatorLights2"]
            statusIndicatorLights3 = form.cleaned_data["statusIndicatorLights3"]
            if serial[0:4] == "24-X":
                theResponse = "please upgrade your device"

            elif serial[0:4] == "36-X":
                if statusIndicatorLights1 == "off" and statusIndicatorLights2 == "off" and statusIndicatorLights3 == "off":
                    theResponse = "turn on the device"
                elif statusIndicatorLights1 == "on" and statusIndicatorLights2 == "on" and statusIndicatorLights3 == "on":
                    theResponse = "ALL is ok"
                else:
                    theResponse = "Please wait"

            elif serial[0:4] == "51-B":
                if statusIndicatorLights1 == "off" and statusIndicatorLights2 == "off" and statusIndicatorLights3 == "off":
                    theResponse = "turn on the device"
                elif statusIndicatorLights1 == "blinking" or statusIndicatorLights2 == "blinking" or statusIndicatorLights3 == "blinking":
                    theResponse = "Please wait"
                elif (statusIndicatorLights1 == "on" and statusIndicatorLights2 == "on") or (statusIndicatorLights2 == "on" and statusIndicatorLights3 == "on") or (statusIndicatorLights1 == "on" and statusIndicatorLights3 == "on"):
                    theResponse = "ALL is ok"

            elif serial.isnumeric():
                theResponse = "Bad serial number"

            else:
                theResponse = "Unknown device"

            return render(request, "problemsolver/response.html", {
                "platformResponse": theResponse
            })
        else:
            return render(request, "problemsolver/index.html")
            # return render(request, "problemsolver/response.html", {"platformResponse": theResponse})

    return render(request, "problemsolver/index.html", {
        "form": newProblemForm()
    })
