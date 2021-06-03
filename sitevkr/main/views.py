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
    if status_file != "":
        context = {"button_label": "Упс, с вашим CSV файлом что-то не так"}
        return render(request, 'main/addbutton.html', context)
    context = {"button_label": "Выберете CSV файл"}

    return render(request, 'main/addbutton.html', context)


def calc(request, name_file):
    try:
        data = pd.read_csv("media/csv/"+name_file, decimal=",", delimiter=';')
        content = {'graph': False, "name_file": name_file, 'csv': False}
        result = []
        if request.method == 'POST':
            form = request.POST
            if 'type_date' in form:
                latitude = int(form['latitude'])
                tilt_angle = int(form['tilt_angle'])
                azimuth = int(form['azimuth'])
                content.update({'latitude': latitude,
                                'tilt_angle': tilt_angle,
                                'azimuth': azimuth,
                                'csv': True})
                if form['type_date'] == 'day':
                    nmon = int(form['nmon_day'])
                    nday = int(form['nday_day'])
                    content.update({"nmon": nmon, "nday": nday})
                    if form['select_day'] == 'sd1':
                        content.update({"table": 'hour'})
                        result = utils.calc_day_by_hours(data, nmon, nday, latitude, tilt_angle, azimuth)
                        if 'check_graph_day' in form:
                            graph_data = [[i + 1, result[i]] for i in range(len(result))]
                            content.update({'graph': True,
                                       'data': graph_data,
                                       'title': f'Полученная энергия на наклонной поверхности за {nday}-й день {nmon}-го месяца',
                                       'xAxis': "Час"})
                        if 'check_max_titl' in form:
                            max_titl = utils.max_tilt_angle(utils.calc_day_by_hours, data, nmon, nday,
                                                            latitude=latitude, azimuth=azimuth)
                            content.update({"name_file": name_file, "max_titl": max_titl})

                elif form['type_date'] == 'month':
                    nmon = int(form['nmon_mon'])
                    content.update({"nmon": nmon})
                    if form['select_month'] == 'sm1':
                        content.update({"table": 'hour'})
                        result = utils.calc_month_by_hours(data, nmon, latitude, tilt_angle, azimuth)
                        if 'check_max_titl' in form:
                            max_titl = utils.max_tilt_angle(utils.calc_month_by_hours, data, nmon,
                                                            latitude=latitude, azimuth=azimuth)
                            content.update({"name_file": name_file, "max_titl": max_titl})

                    elif form['select_month'] == 'sm2':
                        content.update({"table": 'day'})
                        result = utils.calc_month_by_day(data, nmon, latitude, tilt_angle, azimuth)
                        if 'check_graph_month' in form:
                            graph_data = [[i + 1, result[i]] for i in range(len(result))]
                            content.update({'graph': True,
                                       'data': graph_data,
                                       'title': f'Полученная энергия на наклонной поверхности за {nmon}-й месяц',
                                       'xAxis': "День"})
                        if 'check_max_titl' in form:
                            max_titl = utils.max_tilt_angle(utils.calc_month_by_day, data, nmon,
                                                            latitude=latitude, azimuth=azimuth)
                            content.update({"name_file": name_file, "max_titl": max_titl})

                elif form['type_date'] == 'year':
                    if form['select_year'] == 'sy1':
                        content.update({"table": 'hour'})
                        result = utils.calc_year_by_hours(data, latitude, tilt_angle, azimuth)
                        if 'check_max_titl' in form:
                            max_titl = utils.max_tilt_angle(utils.calc_year_by_hours, data,
                                                            latitude=latitude, azimuth=azimuth)
                            content.update({"name_file": name_file, "max_titl": max_titl})

                    elif form['select_year'] == 'sy2':
                        content.update({"table": 'day'})
                        result = utils.calc_year_by_day(data, latitude, tilt_angle, azimuth)
                        if 'check_max_titl' in form:
                            max_titl = utils.max_tilt_angle(utils.calc_year_by_day, data,
                                                            latitude=latitude, azimuth=azimuth)
                            content.update({"name_file": name_file, "max_titl": max_titl})

                    elif form['select_year'] == 'sy3':
                        content.update({"table": 'month'})
                        result = utils.calc_year_by_month(data, latitude, tilt_angle, azimuth)
                        if 'check_graph_year' in form:
                            graph_data = [[i + 1, result[i]] for i in range(len(result))]
                            content.update({'graph': True,
                                       'data': graph_data,
                                       'title': f'Полученная энергия на наклонной поверхности за год',
                                       'xAxis': "Месяц"})
                        if 'check_max_titl' in form:
                            max_titl = utils.max_tilt_angle(utils.calc_year_by_month, data,
                                                            latitude=latitude, azimuth=azimuth)
                            content.update({"name_file": name_file, "max_titl": max_titl})

                elif form['type_date'] == 'custom':
                    if form['select_custom'] == 'sc1':
                        content.update({"table": 'hour'})
                        nmon1 = int(form['nmon_cus1'])
                        nday1 = int(form['nday_cus1'])
                        nmon2 = int(form['nmon_cus2'])
                        nday2 = int(form['nday_cus2'])
                        result = utils.calc_by_range(data, nmon1, nday1, nmon2, nday2, latitude, tilt_angle, azimuth)
                        content.update({"nmon1": nmon1, "nday1": nday1,
                                        "nmon2": nmon2, "nday2": nday2 })
                        if 'check_max_titl' in form:
                            max_titl = utils.max_tilt_angle(utils.calc_by_range, data, nmon1, nday1, nmon2, nday2,
                                                            latitude=latitude, azimuth=azimuth)
                            content.update({"name_file": name_file, "max_titl": max_titl})

                request.session['result'] = pd.Series(result).to_json(orient='values')
                table, columns = data_table(request, content)
                content.update({"table": table, "columns": columns})
        return render(request, 'main/calc.html', content)
    except (IndexError, ValueError, KeyErro):
        # TypeError, AttributeError
        return redirect(reverse('file_false', kwargs={'status_file': name_file+'_false'}))


def data_table(request, content):
    name_file = content['name_file']
    data = pd.read_csv("media/csv/" + name_file, decimal=",", delimiter=';')
    if ('nmon' in content) and ('nday' in content) :
        data = data.loc[(data["Month"] == int(content['nmon'])) &
                        (data["Day"] == int(content['nday']))]
    elif 'nmon' in content:
        data = data.loc[(data["Month"] == int(content['nmon']))]
    elif 'nmon1' in content:
        data = data[(data.Month >= int(content['nmon1'])) & (data.Month <= int(content['nmon2']))]
        data = data.drop(data[(data.Month == int(content['nmon1'])) &
                              (data.Day < int(content['nday1']))].index)
        data = data.drop(data[(data.Month == int(content['nmon2'])) &
                              (data.Day > int(content['nday2']))].index)

    result = [float(s) for s in list(filter(None, request.session.get('result')[1: -1].split(',')))]
    if content["table"] == 'hour':
        month = list(data.Month)
        day = list(data.Day)
        hour = list(data.Hour)
        return [[month[i], day[i], hour[i], result[i]] for i in range(len(result))], 4
    if content["table"] == 'day':
        if len(result) <= 31:
            month = list(data.Month)
            day = list(set(data.Day))
            return [[month[i], day[i], result[i]] for i in range(len(result))], 3
        else:
            data = data.drop(data[data.Hour != 1].index)
            month = list(data.Month)
            day = list(data.Day)
            return [[month[i], day[i], result[i]] for i in range(len(result))], 3
    if content["table"] == 'month':
        month = list(set(data.Month))
        return [[month[i], result[i]] for i in range(len(result))], 2



def download_csv(request):
    name_file = 'test.csv'
    if request.method == 'GET':
        name_file = request.GET.get('name_file')
        data = pd.read_csv("media/csv/" + name_file, decimal=",", delimiter=';')
        data = data.drop(data.columns[[0]], axis=1)
        if request.GET.get('nmon') != '' and request.GET.get('nday') != '':
            data = data.loc[(data["Month"] == int(request.GET.get('nmon'))) &
                            (data["Day"] == int(request.GET.get('nday')))]
        elif request.GET.get('nmon') != '':
            data = data.loc[(data["Month"] == int(request.GET.get('nmon')))]
        elif request.GET.get('nmon1') != '':
            data = data[(data.Month >= int(request.GET.get('nmon1'))) & (data.Month <= int(request.GET.get('nmon2')))]
            data = data.drop(data[(data.Month == int(request.GET.get('nmon1'))) &
                                  (data.Day < int(request.GET.get('nday1')))].index)
            data = data.drop(data[(data.Month == int(request.GET.get('nmon2'))) &
                                  (data.Day > int(request.GET.get('nday2')))].index)
        data['GOI'] = [float(s) for s in list(filter(None, request.session.get('result')[1: -1].split(',')))]
        data.to_csv("media/export_csv/new_" + name_file, sep=';')
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    # Define the full file path
    filepath = BASE_DIR + '/media/export_csv/new_' + name_file
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % "new_"+name_file
    # Return the response value
    if os.path.exists("media/export_csv/new_" + name_file):
        os.remove("media/export_csv/new_" + name_file)
    return response


def select_columns(request, name_file):
    print("1")
    return render(request, 'main/select_columns.html')