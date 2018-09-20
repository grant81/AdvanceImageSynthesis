#!/usr/bin/env python3

import os, sys
import base64
import hashlib
import numpy as np
import argparse
import json
from bs4 import BeautifulSoup as bs
import OpenEXR
import Imath
from PIL import Image


HTML_TEMPLATE = '''<!DOCTYPE html> <html> <head> <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/> <meta content="width=device-width, initial-scale=1.0" name="viewport"/> <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script> <script type="text/javascript">!function(t){t.fn.twentytwenty=function(e){e=t.extend({default_offset_pct_x:.5,default_offset_pct_y:.5,click_needed:!1},e);return this.each(function(){for(var c=e.default_offset_pct_x,h=e.default_offset_pct_y,w=t(this),n=(e.click_needed,w.children("img").length),i=[w.children("img:eq(0)"),w.children("img:eq(1)"),w.children("img:eq(2)"),w.children("img:eq(3)")],s=0,d=0,f=0;f<n;f++)s<i[f].get(0).naturalWidth&&(s=i[f].get(0).naturalWidth,d=f);w.css("max-width",i[d].get(0).naturalWidth),w.addClass("twentytwenty-compare-"+n);for(f=0;f<n;f++)i[f].addClass("twentytwenty-"+(f+1));w.append("<div class='twentytwenty-overlay'></div>");var a=w.find(".twentytwenty-overlay");for(f=0;f<n;f++)a.append("<div class='twentytwenty-label-"+(f+1)+"'>"+i[f].attr("alt")+"</div>");var r=[a.find(".twentytwenty-label-1"),a.find(".twentytwenty-label-2"),a.find(".twentytwenty-label-3"),a.find(".twentytwenty-label-4")];for(f=0;f<n;f++)a.append("<div class='twentytwenty-frame-"+(f+1)+"'></div>");a.find(".twentytwenty-frame-1"),a.find(".twentytwenty-frame-2"),a.find(".twentytwenty-frame-3"),a.find(".twentytwenty-frame-4");var l=[a.find(".twentytwenty-frame-1"),a.find(".twentytwenty-frame-2"),a.find(".twentytwenty-frame-3"),a.find(".twentytwenty-frame-4")],y=function(t,e){var c,h,s,f,y,o=(c=t,h=e,s=i[d].width(),f=i[d].height(),{w:s+"px",h:f+"px",cw:c*s+"px",ch:h*f+"px",w2:s,h2:f,cw2:c*s,ch2:h*f});y=o,a.css("width",y.w),a.css("height",y.h),2==n?(i[0].css("clip","rect(0,"+y.cw+","+y.h+",0)"),r[0].css({right:y.w2-y.cw2}),r[1].css({left:y.cw2}),l[0].css({width:y.cw2,height:y.h2}),l[1].css({width:y.w2-y.cw2,height:y.h2})):3==n?(i[0].css("clip","rect(0,"+y.cw+","+y.ch+",0)"),i[1].css("clip","rect(0,"+y.w+","+y.ch+","+y.cw+")"),i[2].css("clip","rect("+y.ch+","+y.w+","+y.h+",0)"),l[0].css({width:y.cw2,height:y.ch2}),l[1].css({width:y.w2-y.cw2,height:y.ch2}),l[2].css({width:y.w2,height:y.h2-y.ch2}),r[0].css({right:y.w2-y.cw2,bottom:y.h2-y.ch2}),r[1].css({left:y.cw2,bottom:y.h2-y.ch2}),r[2].css({top:y.ch2})):4==n&&(i[0].css("clip","rect(0,"+y.cw+","+y.ch+",0)"),i[1].css("clip","rect(0,"+y.w+","+y.ch+","+y.cw+")"),i[2].css("clip","rect("+y.ch+","+y.cw+","+y.h+",0)"),i[3].css("clip","rect("+y.ch+","+y.w+","+y.h+","+y.cw+")"),l[0].css({width:y.cw2,height:y.ch2}),l[1].css({width:y.w2-y.cw2,height:y.ch2}),l[2].css({width:y.cw2,height:y.h2-y.ch2}),l[3].css({width:y.w2-y.cw2,height:y.h2-y.ch2}),r[0].css({right:y.w2-y.cw2,bottom:y.h2-y.ch2}),r[1].css({left:y.cw2,bottom:y.h2-y.ch2}),r[2].css({right:y.w2-y.cw2,top:y.ch2}),r[3].css({left:y.cw2,top:y.ch2})),w.css("height",y.h)};t(window).on("resize.twentytwenty",function(t){for(var e=0;e<n;e++)e!=d&&(i[e].css("width",i[d].width()),i[e].css("height",i[d].height()));y(c,h)}),w.on("move mousemove",function(t){c=Math.max(0,Math.min(1,(t.pageX-w.offset().left)/i[d].width())),h=Math.max(0,Math.min(1,(t.pageY-w.offset().top)/i[d].height())),y(c,h)}),w.find("img").on("mousedown",function(t){t.preventDefault()}),t(window).trigger("resize.twentytwenty")})}}(jQuery); </script> <script>$(window).load(function(){$(".twentytwenty-container").twentytwenty({default_offset_pct: 0.5});});</script></script> <style>
.subtitle,.title{text-align:center}body{color:#333;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";font-size:16px}.container{margin:0 auto 100px;max-width:900px}.title{font-size:32px;font-weight:500}#course{padding-top:100px}#assignment{padding-bottom:30px}.subtitle{font-weight:400;font-size:21px;padding-bottom:4px}#firstlast{font-size:28px;font-variant:small-caps}.metadata{padding-bottom:30px}h1,h2,h3,h4{font-weight:500;padding-top:24px;line-height:100%;}h1{font-size:25px;padding-bottom:8px;border-bottom:1px solid #eee}h2{font-size:22px}h3{font-size:20px}h4{font-size:18px}.twentytwenty-container{-webkit-box-sizing:content-box;-moz-box-sizing:content-box;box-sizing:content-box;overflow:hidden;position:relative;-webkit-user-select:none;-moz-user-select:none;margin:0 auto;border:2px solid #000;display:block}.twentytwenty-container img{position:absolute;top:0;display:block;max-width:100%;height:auto}.twentytwenty-container *{-webkit-box-sizing:content-box;-moz-box-sizing:content-box;box-sizing:content-box}.twentytwenty-frame-1,.twentytwenty-frame-2,.twentytwenty-frame-3,.twentytwenty-frame-4{position:absolute;display:block;z-index:30;-webkit-box-shadow:0 0 12px rgba(0,0,0,.5);-moz-box-shadow:0 0 12px rgba(0,0,0,.5);box-shadow:0 0 12px rgba(0,0,0,.5)}.twentytwenty-compare-2 .twentytwenty-frame-1{border-right:1px solid #fff;top:0;left:0;cursor:col-resize}.twentytwenty-compare-2 .twentytwenty-frame-2{border-left:1px solid #fff;top:0;right:0;cursor:col-resize}.twentytwenty-compare-3 .twentytwenty-frame-1,.twentytwenty-compare-4 .twentytwenty-frame-1{border-right:1px solid #fff;border-bottom:1px solid #fff;top:0;left:0;cursor:move}.twentytwenty-compare-3 .twentytwenty-frame-2,.twentytwenty-compare-4 .twentytwenty-frame-2{border-left:1px solid #fff;border-bottom:1px solid #fff;top:0;right:0;cursor:move}.twentytwenty-compare-3 .twentytwenty-frame-3{border-top:1px solid #fff;bottom:0;cursor:move}.twentytwenty-compare-4 .twentytwenty-frame-3{border-right:1px solid #fff;border-top:1px solid #fff;bottom:0;left:0;cursor:move}.twentytwenty-compare-4 .twentytwenty-frame-4{border-left:1px solid #fff;border-top:1px solid #fff;bottom:0;right:0;cursor:move}.twentytwenty-overlay{position:relative;z-index:25;overflow:hidden}.twentytwenty-1{z-index:20}.twentytwenty-2{z-index:10}.twentytwenty-3{z-index:9}.twentytwenty-4{z-index:8}.twentytwenty-label-1,.twentytwenty-label-2,.twentytwenty-label-3,.twentytwenty-label-4{position:absolute;text-shadow:0 0 .5ex #000,0 0 .5ex #000;color:#fff;font-size:18px;padding:1ex;overflow:hidden;text-align:center;bottom:0}.twentytwenty-compare-3 .twentytwenty-label-3{width:100%}
</style> <title>A1 | John Doe</title> </head> <body> <div class="container"> <div class="title" id="course">ECSE 446: Realistic Image Synthesis</div><div class="title" id="assignment">Assignment 1</div><div class="metadata"> <div class="subtitle" id="firstlast">John Doe</div><div class="subtitle" id="id">123456789</div></div><div id="renders"> </div></div></body> </html>'''


def convert_exr(input_file, output_file, filetype='PNG'):
    """Convert OpenEXR to PNG/JPG file"""

    # Read OpenEXR file
    src = OpenEXR.InputFile(input_file)
    pixel_type = Imath.PixelType(Imath.PixelType.FLOAT)
    dw = src.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    # Convert linear to sRGB (gamma correction)
    rgb = [np.frombuffer(src.channel(c, pixel_type), dtype=np.float32) for c in 'RGB']
    for i in range(3):
        rgb[i] = np.where(rgb[i] <= 0.0031308,
                (rgb[i] * 12.92) * 255.,
                (1.055 * (rgb[i] ** (1. / 2.4)) - 0.055) * 255.)

    # Write to file
    rgb8 = [Image.frombytes('F', size, c.tostring()).convert('L') for c in rgb]
    Image.merge('RGB', rgb8).save(output_file, filetype, quality=100)


def build_submission(config):
    """Build student assignment submission"""

    soup = bs(HTML_TEMPLATE, 'html5lib')

    # Set title
    title = soup.find('title')
    title.clear()
    my_title = 'A{} | {}'.format(config['assignment'], config['firstlast'])
    title.append(my_title)

    # Set course title
    course = soup.find(id='course')
    course.clear()
    if config['course'] == 446:
        course_title = 'ECSE 446: Realistic Image Synthesis'
    elif config['course'] == 546:
        course_title  = 'ECSE 546: Advanced Image Synthesis'
    elif config['course'] == 598:
        course_title = 'COMP 598: Realistic Image Synthesis'
    else:
        raise ValueError('Error: invalid course number')
    course.append(course_title)

    # Set assignment number
    assignment = soup.find(id='assignment')
    assignment.clear()
    assignment.append('Assignment {}'.format(config['assignment']))

    # Set student's name
    name = soup.find(id='firstlast')
    name.clear()
    name.append(config['firstlast'])

    # Set student's ID
    id = soup.find(id='id')
    id.clear()
    id.append(bs('ID <code>{}</code>'.format(config['id']), 'html5lib'))

    # Create directory for convert images
    if not os.path.exists('pngs'):
        os.makedirs('pngs')

    # Insert all rendered scenes
    renders = soup.find(id='renders')
    for i, task in enumerate(config['renders']):
        slider = '<h1>{}</h1>\n'.format(task['scene'])
        slider_title = task['scene'].replace(' ', '_').lower()
        convert_exr(task['render'], 'pngs/{}.png'.format(slider_title))
        slider += build_slider(slider_title)
        renders.append(bs(slider, 'html.parser'))

    # Save
    output = 'a{}_{}.html'.format(config['assignment'], config['id'])
    with open(output, 'w') as out_f:
        out_f.write(str(soup))


def build_slider(scene_title):
    """ Build HTML section with slider for scene"""

    ref_render = '../refs/{}.png'.format(scene_title)
    submit_render = 'pngs/{}.png'.format(scene_title)
    slider = '<div class="twentytwenty-container">\n'
    slider += '  <img alt="Reference" src="{}"/>\n'.format(ref_render)
    with open(submit_render, 'rb') as img_f:
        img_64 = base64.b64encode(img_f.read()).decode('utf-8')
        slider += '  <img alt="Submission" src="data:image/png;base64,{}"/>\n'.format(img_64)
    slider += "</div>\n"
    return slider


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Assignment submission for ECSE 446/546')
    parser.add_argument('config', help='configuration file', type=str)
    args = parser.parse_args()

     # Check argument formats
    if not args.config.lower().endswith('.json'):
        raise ValueError('Input tasks must be a JSON file')

    # Read JSON file
    try:
        with open(args.config) as f:
            config = json.load(f)
    except:
        raise ValueError('Error: cannot open config file')

    # Check if config file is correct
    keys = ['firstlast', 'id', 'assignment', 'course', 'renders']
    formatted = True
    for key in keys:
        if config.get(key) is None: formatted = False
    if not formatted:
        raise ValueError('Error: something is wrong with the config file')

    # Create HTML submission
    build_submission(config)
