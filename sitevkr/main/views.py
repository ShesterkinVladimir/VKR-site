from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import Upload_Form
import utils
import pandas as pd
import numpy as np
import mimetypes
from django.http.response import HttpResponse
import os


def upload_file(request, status_file=""):  # загрузка файла по нажатию кнопки
    if request.method == 'POST':
        form = Upload_Form(request.POST, request.FILES)
        if form.is_valid():
            newfile = form.save(commit=False)
            newfile.file = request.FILES['file']
            file_type = newfile.file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type != 'csv':
                context = {"button_label": "Был выбран не CSV файл. Попробуйте еще раз", }
                return render(request, 'main/addbutton.html', context)
            newfile.save()
            return redirect('calc/'+str(newfile.file))
            # return redirect('select_columns/'+str(newfile.file))
    if status_file != "":
        context = {"button_label": "Упс, с вашим CSV файлом что-то не так"}
        return render(request, 'main/addbutton.html', context)
    context = {"button_label": "Выберете CSV файл"}
    return render(request, 'main/addbutton.html', context)


def calc(request, name_file):
    try:
        data = pd.read_csv("media/csv/"+name_file, decimal=",", delimiter=';')
        content = {'graph ': False}
        if request.method == 'POST':
            form = request.POST
            if 'type_date' in form:
                latitude = int(form['latitude'])
                tilt_angle = int(form['tilt_angle'])
                azimuth = int(form['azimuth'])
                if form['type_date'] == 'day':
                    nmon = int(form['nmon_day'])
                    nday = int(form['nday_day'])
                    if form['select_day'] == 'sd1':
                        day_by_hours = utils.calc_day_by_hours(data, nmon, nday, latitude, tilt_angle, azimuth)
                        data_graph = []
                        for i in range(len(day_by_hours)):
                            data_graph.append([i+1, day_by_hours[i]])
                        if 'check_graph_day' in form:
                            content = {'graph': True,
                                       'data': data_graph,
                                       'title': f'Полученная энергия на наклонной поверхности за {nday}-й день {nmon}-го месяца',
                                       'xAxis': "Час"}
                        if 'check_max_titl' in form:
                            max_titl = utils.max_tilt_angle(utils.calc_day_by_hours, data, nmon, nday,
                                                            latitude=latitude, azimuth=azimuth)
                elif form['type_date'] == 'month':
                    nmon = int(form['nmon_mon'])
                    if form['select_month'] == 'sm1':
                        month_by_hours = utils.calc_month_by_hours(data, nmon, latitude, tilt_angle, azimuth)
                        if 'check_max_titl' in form:
                            max_titl = utils.max_tilt_angle(utils.calc_month_by_hours, data, nmon,
                                                            latitude=latitude, azimuth=azimuth)
                    elif form['select_month'] == 'sm2':
                        month_by_day = utils.calc_month_by_day(data, nmon, latitude, tilt_angle, azimuth)
                        data_graph = []
                        for i in range(len(month_by_day)):
                            data_graph.append([i + 1,  month_by_day[i]])
                        if 'check_graph_month' in form:
                            content = {'graph': True,
                                       'data': data_graph,
                                       'title': f'Полученная энергия на наклонной поверхности за {nmon}-й месяц',
                                       'xAxis': "День"}
                        if 'check_max_titl' in form:
                            max_titl = utils.max_tilt_angle(utils.calc_month_by_day, data, nmon,
                                                            latitude=latitude, azimuth=azimuth)
                elif form['type_date'] == 'year':
                    if form['select_year'] == 'sy1':
                        year_by_hours = utils.calc_year_by_hours(data, latitude, tilt_angle, azimuth)
                        if 'check_max_titl' in form:
                            max_titl = utils.max_tilt_angle(utils.calc_year_by_hours, data,
                                                            latitude=latitude, azimuth=azimuth)
                    elif form['select_year'] == 'sy2':
                        year_by_day = utils.calc_year_by_day(data, latitude, tilt_angle, azimuth)
                        if 'check_max_titl' in form:
                            max_titl = utils.max_tilt_angle(utils.calc_year_by_day, data,
                                                            latitude=latitude, azimuth=azimuth)
                    elif form['select_year'] == 'sy3':
                        year_by_month = utils.calc_year_by_month(data, latitude, tilt_angle, azimuth)
                        data_graph = []
                        for i in range(len(year_by_month)):
                            data_graph.append([i + 1, year_by_month[i]])
                        if 'check_graph_year' in form:
                            content = {'graph': True,
                                       'data': data_graph,
                                       'title': f'Полученная энергия на наклонной поверхности за год',
                                       'xAxis': "Месяц"}
                        if 'check_max_titl' in form:
                            max_titl = utils.max_tilt_angle(utils.calc_year_by_month, data,
                                                            latitude=latitude, azimuth=azimuth)

                elif form['type_date'] == 'custom':
                    if form['select_custom'] == 'sc1':
                        nmon1 = int(form['nmon_cus1'])
                        nday1 = int(form['nday_cus1'])
                        nmon2 = int(form['nmon_cus2'])
                        nday2 = int(form['nday_cus2'])
                        calc_by_range = utils.calc_by_range(data, nmon1, nday1, nmon2, nday2, latitude, tilt_angle, azimuth)
                        if 'check_max_titl' in form:
                            max_titl = utils.max_tilt_angle(utils.calc_by_range, data, nmon1, nday1, nmon2, nday2,
                                                            latitude=latitude, azimuth=azimuth)
            # content.update({"form": form})
        content.update({"name_file":  name_file})
        return render(request, 'main/calc.html', content)
    except (TypeError, AttributeError):
        return redirect(reverse('file_false', kwargs={'status_file': name_file+'_false'}))


def download_csv(request):
    name_file = 'test.csv'
    if request.method == 'GET':
        name_file = request.GET.get('name_file')
        data = pd.read_csv("media/csv/" + name_file, decimal=",", delimiter=';')
        sLength = len(data['HOY'])
        data['a'] = pd.Series(np.random.randn(sLength), index=data.index)
        data.to_csv("media/export_csv/new_" + name_file, sep=';')
        print(data)
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = name_file
    # Define the full file path
    filepath = BASE_DIR + '/media/csv/' + filename
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % "new_"+filename
    # Return the response value
    if os.path.exists("media/export_csv/new_" + name_file):
        os.remove("media/export_csv/new_" + name_file)
    return response


def select_columns(request, name_file):
    print("1")
    return render(request, 'main/select_columns.html')