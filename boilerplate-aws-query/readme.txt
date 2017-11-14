(PG note: this directory code is aws-submitted sample code for downloading from their top sites API, found here: https://aws.amazon.com/code/query-example-in-java/?tag=code%23keywords%23alexa-top-sites --- and soon to be slightly modified after testing.)  Using country code US.

-------------------------------------------------------------------------
-                      Java Sample for Alexa Top Sites                  -
-------------------------------------------------------------------------
This sample will make a request to the Alexa Top Sites web service 
using your Access Key ID and Secret Access Key.

Tested with Java version 1.6.

Steps:
1. Sign up for an Amazon Web Services account at http://aws.amazon.com
   (Note that you must have a valid credit card)
2. Get your Access Key ID and Secret Access Key
3. Sign up for Alexa Top Sites at http://aws.amazon.com/alexatopsites
4. Uncompress the zip file into a working directory
5. Compile TopSites.java:

    javac TopSites.java

6. Run

    java TopSites ACCESS_KEY_ID SECRET_ACCESS_KEY [COUNTRY_CODE]

Country code is optional.

If you are getting "Not Authorized" messages, you probably have one of the
following problems:

1. Your access key or secret key were not entered properly.  Please re-check
that they are correct.

2. You did not sign up for Alexa Top Sites at
http://aws.amazon.com/alexatopsites (This step is separate from signing 
up for Amazon Web Services.)

3. Your credit card was not valid.

If you are getting "Request Expired" messages, please check that the date 
and time are properly set on your computer.
