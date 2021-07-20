#!/usr/bin/python3

import argparse
from fpdf import FPDF
from llog import LLogReader
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_pdf import PdfPages

dir_path = os.path.dirname(os.path.realpath(__file__))
defaultMeta = dir_path+'/kellerld.meta'

parser = argparse.ArgumentParser(description='kellerld test report')
parser.add_argument('--input', action='store', type=str, required=True)
# parser.add_argument('--output-dir', action='store', type=str, required=True)
parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
args = parser.parse_args()

log = LLogReader(args.input, args.meta)

p = log.data.pressure
t = log.data.temperature

p.ll.pplot(t)
plt.title('KellerLD Pressure + Temperature')

plt.figure()
log.data.ll.plot(['temperature', 'pressure'], ['temperature'])



pdf = FPDF()
pdf.add_page()
pdf.set_font('Courier')
epw = pdf.w - 2*pdf.l_margin

def table(df, title):
    widths = {}
    for c in df:
        widths[c] = pdf.get_string_width(c)
        for r in df[c]:
            d = str(r)
            width = pdf.get_string_width(d)
            print(c, d, width)
            if width > widths[c]:
                print('upgrading')
                widths[c] = width

    for key, value in widths.items():
        print(key, value)
        widths[key] = value+2
    
    # total table width
    twidth = sum(widths.values())

    pdf.cell(twidth, 4, title, border=1)
    pdf.ln(4)
    # print column names
    for c in df:
        pdf.cell(widths[c], 4, c, border=1)
    pdf.ln(4)
    for r in df.index:
        for c in df:
            pdf.cell(widths[c], 4, str(df[c][r]), border=1)
    pdf.ln(4)

def plot(df):
    df.plot(figsize=(20,5))
    tfile = '/tmp/x.png'
    plt.savefig(tfile)
    plt.close()

    pdf.image(tfile, w=epw)
    
#https://stackoverflow.com/a/59574470

table(log.rom, 'rom values')
plot(log.data.pressure)
plot(log.data.temperature)
pdf.output('test.pdf')

with PdfPages('test2.pdf') as pdf:
    log.data.temperature.ll.plot()
    pdf.savefig()
    log.data.pressure.ll.plot()
    pdf.savefig()

    fig = plt.figure()
    ax = fig.add_subplot()
    # ax.axis('tight')
    # ax.axis('off')
    # ax.table(cellText=[['title']], loc='bottom',
    # bbox = [0,0,1.0, 0.1]
    # )
    # ax.axis('off')

    log.rom.style.set_table_attributes("style='display:inline'").set_caption('Caption table')
    # ax.table(cellText=log.rom.values, colLabels=log.rom.columns, loc='center')
    # ax.set_ylabel('y')
    # ax.set_xlabel('z')
    t= ax.table(cellText=log.rom.to_numpy(dtype=str), colLabels=log.rom.columns, loc='upper center', cellLoc='center')
    # t.auto_set_font_size(True)


    # t = pd.plotting.table(ax, log.rom, colLabels=log.rom.columns, loc='upper left')
    ax.set_title('hello')

    # plt.show()
    # t = pd.plotting.table(ax, log.data.iloc[:12 , :], rowLabels=[''])
    # t.auto_set_font_size(False)
    # t.set_fontsize(24)
    # ax.axis('tight')
    # plt.show()
    pdf.savefig()

    header = plt.table(cellText=[['']*2],
                      colLabels=['Extra header 1', 'Extra header 2'],
                      loc='bottom'
                      )

    # the_table = plt.table(cellText=cell_text,
    #                   rowLabels=rows,
    #                   rowColours=colors,
    #                   colLabels=columns,
    #                   loc='bottom',
    #                   bbox=[0, -0.35, 1.0, 0.3]
    #                   )
    plt.show()

# fig, axs = plt.subplots(2, 1, figsize=(8.5,11.0))

# axs[0].table(cellText=log.rom.to_numpy(dtype=str), colLabels=log.rom.columns, loc='upper center', cellLoc='center', fontsize=18)
# log.data.pressure.ll.plot(axs[1])
# plt.show()
f = plt.figure(figsize=(8.5,11.0))
ax = f.add_subplot(3, 1, 1)
t = ax.table(cellText=log.rom.to_numpy(dtype=str), colLabels=log.rom.columns, loc='bottom', cellLoc='center', bbox=[0,0.5,1,0.5])
t.auto_set_font_size(False)
t.set_fontsize(12)
ax.set_title("hello")

ax = f.add_subplot(3, 1, (2,3))
log.data.pressure.ll.plot(ax)
plt.show()



f = plt.figure(figsize=(8.5,11.0))

f.suptitle('KellerLD Test Report')
height_ratios=[1,8,8]
spec = f.add_gridspec(len(height_ratios), 2, height_ratios=height_ratios)

# plot table
ax = f.add_subplot(spec[0,:])
t = ax.table(cellText=log.rom.to_numpy(dtype=str), colLabels=log.rom.columns, loc='bottom', cellLoc='center', bbox=[0,0,1,1])
t.auto_set_font_size(False)
t.set_fontsize(12)
ax.set_title("KellerLD ROM Configuration")
ax.axis('off')

ax = f.add_subplot(spec[1:,:])
log.data.ll.plot(['temperature'], ['pressure'])
plt.show()
# def table_helper(pdf, epw, th, table_data, col_num):
#     for row in table_data:
#         maxwidth=0
#         for datum in row:
#             d = str(datum)
#             w = pdf.get_string_width(d)
#             if w > maxwidth:
#                 maxwidth = w
#         for datum in row:
#             # Enter data in columns
#             d = str(datum)
#             pdf.cell(maxwidth + 2, 2 * th, d, border=1)
#         pdf.ln(2 * th)
