import boto3
import zipfile
import StringIO


def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:224431210594:deployPortfolioTopic')

    location = {
        "bucketName":'portfoliobuild.panharithchhum.com',
        "objectKey": 'portfolioBuild.zip'
    }
    try:
        job = event.get("CodePipeline.job")

        if job:
            print "Lambda triggered form codepipeline event"
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "MyAppBuild":
                    location = artifact["location"]["s3Location"]

        print "Building portfolio from " + str(location)

        s3 = boto3.resource('s3')

        portfolio_bucket = s3.Bucket('portfolio.panharithchhum.com')
        build_bucket = s3.Bucket(location["bucketName"])

        portfolio_zip = StringIO.StringIO()

        build_bucket.download_fileobj(location["objectKey"], portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                if not nm.startswith('.git'):
                    obj = myzip.open(nm)
                    portfolio_bucket.upload_fileobj(obj, nm)
                    portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        print "Job done!"

        topic.publish(Subject="Portfolio", Message="Portfolio deployed successfully")

        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject="Portfolio Deploy Failed", Message="Portfolio was not deployed successfully")
        raise

    return 'Hello from Lambda'
