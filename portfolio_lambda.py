def lambda_handler(event, context):
    import StringIO
    import zipfile
    import mimetypes
    import boto3
    from botocore.client import Config
    S3 = boto3.resource('s3', config=Config(signature_version='s3v4'))



    IN_BUCKET = S3.Bucket('biobuild.pouliasis.io')
    OUT_BUCKET = S3.Bucket('bio.pouliasis.io')
    PORTFOLIO_ZIP = StringIO.StringIO()

    IN_BUCKET.download_fileobj('portfoliobuild.zip', PORTFOLIO_ZIP)
    
    with zipfile.ZipFile(PORTFOLIO_ZIP) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            OUT_BUCKET.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
            OUT_BUCKET.Object(nm).Acl().put(ACL='public-read')
    return 'Hello from Lambda'
