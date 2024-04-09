from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from first_app.models import Cloths,SoldItem,Customer
from . import forms
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.enums import TA_CENTER
import pandas as pd
from datetime import datetime
import calendar

def get_names(request):
    search=request.GET.get('search')
    payload=[]
    if search:
        objs=Customer.objects.filter(PhoneNumber__startswith=search)

        for obj in objs:
            payload.append({
                'Name':obj.Name,
                'Age':obj.Age,
                'Phone Number':obj.PhoneNumber
            })

    return JsonResponse({
        'status':True,
        'payload':payload
    })

#SELF CODE DECODE
def decode_word(code, mrp):
    code_mapping = {
        'S': '1', 'I': '2', 'G': '3', 'N': '4', 'A': '5', 'T': '6', 'U': '7',
        'R': '8', 'E': '9', 'O': '0', 'o':'0'
    }
    decoded_word = ''
    for letter in code:
        decoded_word += code_mapping.get(letter.upper(), letter)
    
    decoded_word = int(decoded_word)
    
    if int(mrp) >= decoded_word * 1000:
        decoded_word *= 100
    elif int(mrp) >= decoded_word * 100:
        decoded_word *= 100
    elif int(mrp) >= decoded_word * 10:
        decoded_word *= 10
    elif decoded_word<100:
        decoded_word=decoded_word*10
    
    return decoded_word

#Code for each Product
def calculate_final_code(product):
    final_code = f"{product.Code}{product.Description[2]}{product.Seller[:1]}{product.SIZE}{product.MRP}{(int(product.Date.year)%2000)}"
    return final_code

#genrating pdf 
def generate_pdf(items, total_amount, Name,PhoneNumber,sold_on):
    customer_name=Name
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"attachment; filename={customer_name}.pdf"
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    heading_style = ParagraphStyle(name='Heading', fontSize=20, textColor='black',alignment=TA_CENTER, italic=True)
    heading = Paragraph("MANSI FASHION", heading_style)
    elements.append(heading)
    customer_info = [
        f"Customer Name: {Name}",
        f"Customer Phone Number: {PhoneNumber}",
        f"Date of Purchase:{sold_on}",
        # Add more customer information fields as needed
    ]
    elements.append(Paragraph("<br /><br />"))
    customer_info_paragraph = Paragraph("<br />".join(customer_info), getSampleStyleSheet()['Normal'])
    elements.append(customer_info_paragraph)
    table_data = [
        ["FinalCode", "SIZE", "Description", "Code", "MRP"],
    ]
    for item in items:
        table_data.append([
            item.FinalCode,
            item.SIZE,
            item.Description,
            item.Code,
            item.MRP
        ])
    table_data.append(["", "", "", "Total Amount:", f"\u20B9{total_amount}"])
    table = Table(table_data, colWidths=[70, 50, 200, 70, 70])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])
    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    return response

#Entry Page Code
def Entry(request):
    form=forms.Price()
    if request.method=='POST':
        form=forms.Price(request.POST)
        if form.is_valid():
            print('inside form')
            product = form.save(commit=False)
            product.FinalCode = calculate_final_code(product)
            product.save()
            print('Saved Form')
            return render(request,'Entry.html',{'form':form,'code':product.FinalCode})
        else:
            print('Error')
    return render(request,'Entry.html',{'form':form,'code':"0"})
    

#Billing Page Code
def Billing(request):
    items = Cloths.objects.all()
    if request.method == 'POST':
        Customer_data=request.POST
        Name=Customer_data.get('Name')
        Age=Customer_data.get('Age')
        PhoneNumber=Customer_data.get('autocomplete')
        sold_on=Customer_data.get('Sold_on')
        try:
            Customer.objects.create(Name=Name,Age=Age,PhoneNumber=PhoneNumber)
            print('Customer created successfully!')
        except:
            print('customer Already Exists')
        selected_item_ids = request.POST.getlist('items')
        selected_items = Cloths.objects.filter(pk__in=selected_item_ids)
        selected_total_amount = sum(item.MRP for item in selected_items) 
        for item in selected_items:
            SoldItem.objects.create(Description=item.Description,Seller=item.Seller,Code=item.Code,MRP=item.MRP,Date=item.Date,FinalCode=item.FinalCode,SIZE=item.SIZE,sold_on=sold_on,PhoneNumber=PhoneNumber)
            item.delete()
        return  generate_pdf(selected_items, selected_total_amount,Name=Name,PhoneNumber=PhoneNumber,sold_on=sold_on)
    return render(request, 'billing.html', {'items': items})

#Dashboard Page Code
def Dashboard(request):
    # Extract All the Key Values Pair From the Model
    cloths_data = Cloths.objects.all().values()
    customer_data=Customer.objects.all().values()
    SoldItem_data=SoldItem.objects.all().values()

    # Converting them to Data Frame
    sold_df=pd.DataFrame(list(SoldItem_data))
    sold_df['PhoneNumber'] = sold_df['PhoneNumber'].astype('int64')
    customer_df = pd.DataFrame(list(customer_data))
    customer_df['PhoneNumber'] = customer_df['PhoneNumber'].astype('int64')
    cloths_df = pd.DataFrame(list(cloths_data))

    #Merging Sold and Customers
    merged_df = pd.merge(sold_df, customer_df, on='PhoneNumber', how='inner')

    #Converting initial code to Invested Amount
    cloths_df['Invested'] = cloths_df.apply(lambda row: decode_word(row['Code'], row['MRP']), axis=1)

    #Margin Percentage KPI
    margin_precentage=round(sum(cloths_df['MRP']-cloths_df['Invested'])/sum(cloths_df['MRP'])*100)

    sold_df['sold_on'] = pd.to_datetime(sold_df['sold_on'])
    sold_df['sold_month'] = sold_df['sold_on'].dt.month
    sold_df['sold_month'] = sold_df['sold_month'].apply(lambda x: calendar.month_name[x])

    #Sales Per Month KPI
    k=sold_df[['MRP','sold_month']].groupby('sold_month',as_index=False).sum()
    months=k.sold_month.to_list()
    val=k.MRP.to_list()
    data=cloths_df.SIZE.value_counts().to_dict()
    categories = list(data.keys())
    values = list(data.values())

    #Age Group Demographics
    bins = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
    labels = ['15-20', '20-25', '25-30', '30-35', '35-40', '40-45', '45-50', '50-55', '55-60', '60-65']
    merged_df['Age_Group']=pd.cut(merged_df['Age'], bins=bins, labels=labels, right=False)
    customer_df['Age_Group'] = pd.cut(customer_df['Age'], bins=bins, labels=labels, right=False)
    age_group_counts = customer_df['Age_Group'].value_counts(normalize=True) * 100
    age_group_data = [{'name': group, 'y': round(count,2)} for group, count in age_group_counts.items()]

    #Sale Per Age-Group Demogrphics
    r=merged_df[['Age_Group','PhoneNumber']].groupby('Age_Group',as_index=False).count().sort_values(by='PhoneNumber',ascending=False).iloc[:5,:]
    print(r)
    age_groups=r.Age_Group.tolist()
    No_of_pieces_sold=r.PhoneNumber.tolist()

    #No of Repeat Customers
    unique_data = merged_df.drop_duplicates(subset=['sold_on', 'PhoneNumber'])

    # Count the occurrences of each phone number
    phone_number_counts = unique_data['PhoneNumber'].value_counts()

    filtered_phone_numbers = phone_number_counts[phone_number_counts >= 2]
    # Print the phone number counts 
    print()

    # Prepare chart configuration
    chart_customer_distribution = {
        'chart': {
            'type': 'pie',
            'backgroundColor': 'transparent',
        },
        'title': {
            'text': 'Age Group Percentage Distribution',
            'style': {
                'color': 'white'
            }
        },
        'series': [{
            'name': 'Age Group',
            'data': age_group_data,
        }]
    }

    chart_SALES = {
        'chart': {
            'type': 'line',
            'backgroundColor': 'transparent',  
            'style': {
                'color': 'white'  
            }
        },
        'title': {
            'text': 'Sales Per Month Chart',
            'style': {
                'color': 'white'
            }
        },
        'xAxis': {
            'categories': months,
            'labels': {
                'style': {
                    'color': 'white' 
                }
            },
            'lineColor': 'white',
            'gridLineColor': 'transparent' 
        },
        'yAxis': {
            'title': {
                'text': 'Sales(in Rps)',
                'style': {
                    'color': 'white' 
                }
            },
            'labels': {
                'style': {
                    'color': 'white' 
                }
            },
            'lineColor': 'white',
            'color':'white',
            'gridLineColor': 'transparent' 
        },
        'plotOptions': {
            'column': {
                'borderColor': 'white'
            }
        },
        'series': [{
            'name': 'Months',
            'data': val
        }]
    }
    chart_config = {
        'chart': {
            'type': 'column',
            'backgroundColor': 'transparent',  
            'style': {
                'color': 'white'  
            }
        },
        'title': {
            'text': 'Existing Stock Size Distribution Chart',
            'style': {
                'color': 'white'
            }
        },
        'xAxis': {
            'categories': categories,
            'labels': {
                'style': {
                    'color': 'white' 
                }
            },
            'lineColor': 'white',
            'color':'white',
            'gridLineColor': 'transparent' 
        },
        'yAxis': {
            'title': {
                'text': 'Quantity',
                'style': {
                    'color': 'white' 
                }
            },
            'labels': {
                'style': {
                    'color': 'white' 
                }
            },
            'lineColor': 'white',
            'gridLineColor': 'transparent' 
        },
        'plotOptions': {
            'column': {
                'borderColor': 'white'
            }
        },
        'series': [{
            'name': 'Sizes',
            'data': values
        }]
    }
    percustsales_chart = {
        'chart': {
            'type': 'bar',  # Use 'bar' for horizontal bar chart
            'backgroundColor': 'transparent',
            'style': {
                'color': 'white'
            }
        },
        'title': {
            'text': 'Age-Group vs Pieces Sold',
            'style': {
                'color': 'white'
            }
        },
        'xAxis': {
            'text':'XAXIS',
            'categories': age_groups, 
            'title': {
                'style': {
                    'color': 'white'
                }
            },
            'labels': {
                'title':'Age Group',
                'style': {
                    'color': 'white'
                }
            },
            'lineColor': 'white',
            'gridLineColor': 'transparent'
        },
        'yAxis': {  # Representing categories on y-axis
            'labels': {
                'style': {
                    'color': 'white'
                }
            },
            'lineColor': 'white',
            'color': 'white',
            'gridLineColor': 'transparent'
        },
        'plotOptions': {
            'bar': {
                'borderColor': 'white',
                'color':'red'
            }
        },
        'series': [{
            'name': 'Pieces',
            'data': No_of_pieces_sold
        }]
    }

    return render(request, 'Dashboard.html', {'repeat_customer':len(filtered_phone_numbers),'chart_config': chart_config,'Sales':chart_SALES,'Invested':sum(cloths_df['Invested']),'Margin':margin_precentage,'pieces':len(cloths_df),'Customer':len(customer_df),'Pieces':len(sold_df),'chart_customer_distribution':chart_customer_distribution,'chart':percustsales_chart})


def LoginPage(request):
    if request.method=='POST':
        form=request.POST
        print(form.get('UserID'))
        print(form.get('password'))
        if form.get('UserId')=='Arpit' and form.get('password')=='Arpit':
            return Dashboard(request)
        else:
            raise PermissionError
    return render(request,"loginPage.html")


def index(request):
    return Entry(request)

    
