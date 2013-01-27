#!/usr/bin/python
# coding=UTF-8
# 
# This file has routines related to the configuration information
# of generate_reports script

from generate_report import PdfReport
from generate_report import DirReport
import bc_utils,re

def bc_parse_config_file(PdfReport):
    ifd = open("bc_report_config.txt","r")

    # Clone the static dictionary of file-formats to start with
    # NOTE: The code is retained for future work on letting the user
    # configure the format files. As of now, all format files are
    # generated, but the user can limit the number of these files by setting
    # S:MAX_FILE_FORMAT_FILES_TO_REPORT:20

    PdfReport.bc_config_filefmt_files = DirReport.dictFileFmtStatic.copy() 

    # Initialize all the values to 0
    for x, y in PdfReport.bc_config_filefmt_files.items():
        PdfReport.bc_config_filefmt_files[x] = 0

    # By default, report special files
    PdfReport.bc_config_report_special_files = True

    ## print("D:config_filefmt: ", PdfReport.bc_config_filefmt_files)

    for line in ifd:
        if bc_utils.is_comment_line(line):
            continue 

        line1 = re.split(":", line)
    
        # Set the flag for the particular feature to 1 indicating
        # the user wants to see the report for this feature.
        if line1[0] == 'L':
            ## Logo
            print("Overwriting Logo with", line1[1])
            PdfReport.logo = line1[1]
        elif line1[0] == 'F':
            ## Test if line1[1] is a legitimate feature>
            if line1[1] in PdfReport.bc_config_feature:
                PdfReport.bc_config_feature[line1[1]] = 1

                # if the third field is 0, print all the lines in the
                # feature file. Otherwise print what the number says.
                if line1[2] == '\n':
                    lines = 0
                else:
                    lines = line1[2]
  
                PdfReport.bc_config_feature_lines[line1[1]] = int(lines) 
            else:
                print("Info: Feature %s does NOT exist" % line1[1])
                          

        elif line1[0] == 'R':
            ## Test if line1[1] is a legitimate report file
            if line1[1] in PdfReport.bc_config_report_files:
                PdfReport.bc_config_report_files[line1[1]] = 1
                PdfReport.bc_config_report_lines[line1[1]] = int(line1[2])
                ## print("D: Reporting %d lines for file %s" \
                      ## %(PdfReport.bc_config_report_lines[line1[1]], line1[1]))
            else:
                print("Info: Report file %s is not legitimate" % line1[1])
                print("Info: Fix the config file")
        elif line1[0] == 'M':
            # Get the file format
            file_format = line1[1].rstrip('\n')
           
            # Get all the files that have this format from the dict.
            PdfReport.bc_config_filefmt_files[file_format] = 1
        elif line1[0] == 'S':
            # Find out if user wants special files to be reported
            if line1[1].rstrip() == 'REPORT_SPECIAL_FILES':
                if line1[2].rstrip() == 'YES':
                    PdfReport.bc_config_report_special_files = True
                else:
                    print("D: Not reporting Special files")
                    PdfReport.bc_config_report_special_files = False
            elif line1[1].rstrip() == 'MAX_LINES_TO_REPORT':
                PdfReport.bc_max_lines_to_report = int(line1[2])
            elif line1[1].rstrip() == 'MAX_FILE_FORMAT_FILES_TO_REPORT':
                PdfReport.bc_max_fmtfiles_to_report = int(line1[2])
            elif line1[1].rstrip() == 'MAX_FEATURE_FILES_TO_REPORT':
                PdfReport.bc_max_featfiles_to_report = int(line1[2])
            elif line1[1].rstrip() == 'MAX_FORMATS_FOR_BAR_GRAPH':
                PdfReport.bc_max_formats_in_bar_graph = int(line1[2])

