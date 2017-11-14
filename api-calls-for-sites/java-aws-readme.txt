(PG note: this directory code is aws-submitted sample code for downloading from their top sites API, found here: https://aws.amazon.com/code/query-example-in-java/?tag=code%23keywords%23alexa-top-sites --- and soon to be slightly modified after testing.)  Using country code US.


(PG note 2: I've changed the API to get around 100 sites per call limitation.  With my modifications, the proper call is:

java TopSites ACCESS_KEY_ID SECRET_ACCESS_KEY COUNTRY_CODE NUM_SITES

where both country code and number of sites are mandatory.  This code will now start with #1 and download the top NUM_SITES sites for the given country, broken up in hundred site chunks.  It'll just print them all out as one long list, so it's advisable to redirect it to a file.

I'm going to grab the top 2000 as of November 13, 2017, for the purposes of this research project.)

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
