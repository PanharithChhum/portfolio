import boto3
import zipfile
import StringIO


def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:224431210594:deployPortfolioTopic')

    s3 = boto3.resource('s3')

    try:
        build_bucket = s3.Bucket('portfoliobuild.panharithchhum.com')
        portfolio_bucket = s3.Bucket('portfolio.panharithchhum.com')

        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('portfolioBuild.zip', portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                if not nm.startswith('.git'):
                    obj = myzip.open(nm)
                    portfolio_bucket.upload_fileobj(obj, nm)
                    portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        print "Job done!"

        topic.publish(Subject="Portfolio", Message="Portfolio deployed successfully")
    except:
        topic.publish(Subject="Portfolio Deploy Failed", Message="Portfolio was not deployed successfully")
        raise

    return 'Hello from Lambda'
