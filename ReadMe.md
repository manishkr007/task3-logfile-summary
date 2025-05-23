## Analyze the log file and summarize its results using Python script :-

### Prerequisites :-

1. Python 3.x installed on your system
2. Access to command line/terminal
3. Required Python libraries: re — Regular expression operations (https://docs.python.org/3/library/re.html)

### To run the script :-
python main.py  

### Assumptions :-

1. Printing the results in a new file named analysis_results.txt.
2. Each of request path like /data/wasser/gourmet-wasser/12 and /data/wasser/gourmet-wasser/30 is getting selected in unique request paths. So assuming to keep only generic request path like "/data/wasser/gourmet-wasser" without the number at the end.  
    Similar change applied to rest of all request path as well.  
    However, if that number at the end of request path is required in order to identify any specific item then it can be restored quickly.  

### Common Issues and Resolutions :-

1. Warning: Line did not match regex.  
    Reason: Square bracket on Timestamp and empty square bracket were not handled correctly.  
    Resolution: Tested on file having only 1 record. Updated the regex condition for square bracket on Timestamp and empty square bracket.  