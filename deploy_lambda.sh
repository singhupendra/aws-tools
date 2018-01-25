#!/bin/bash
DIST_ID="E21ZFZT8KOSTCO"
PROFILE="lambda-jubilant"
FUNCTION="stage-getStoreIdByLocation"
REGION="us-east-1"

#Get the latest API version
VERSION=$(aws lambda list-versions-by-function --function-name $FUNCTION --profile $PROFILE  --region $REGION --query 'Versions[].[Version]' --output text | sort -nr | head -1)
echo "Latest version is "$VERSION

#Get the latest ETag for current config
ETAG=$(aws cloudfront get-distribution-config  --id $DIST_ID --profile $PROFILE --query 'ETag'| sed -r 's/"//g' )

echo $ETAG

#get the latest distribution config file
aws cloudfront get-distribution-config  --id $DIST_ID --profile $PROFILE --query 'DistributionConfig' > dist.json

#Get the last version from the distribution
LAST_VERSION=$(grep stage-getStoreIdByLocation:  dist.json | awk '{print $2}' | cut -d":" -f 7,8| sed -r 's/"//g')
echo "The last version was $LAST_VERSION"

#Replace the version in the config file
sed -i "s/$LAST_VERSION/stage-getStoreIdByLocation:$VERSION/g" dist.json

#Update the lambda function arn in the distribution
aws cloudfront update-distribution --id $DIST_ID --distribution-config file://dist.json --profile $PROFILE --if-match $ETAG

#Create invalidations for this deployment
aws cloudfront create-invalidation --distribution-id $DIST_ID --paths /$FUNCTION* --profile $PROFILE
