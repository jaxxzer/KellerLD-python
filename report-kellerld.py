#!/usr/bin/python3

import argparse
from fpdf import FPDF
from llog import LLogReader
import matplotlib.pyplot as plt
import os

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

plt.show()


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
    

table(log.rom, 'rom values')
plot(log.data.pressure)
plot(log.data.temperature)
pdf.output('test.pdf')

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
