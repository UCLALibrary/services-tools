#!/usr/bin/python3

#################################################################################
# Dependencies to use this tool:
# * AWSCLI
# * Default profile in ~/.aws/credentials
# ** Profile needs S3 GET PUT DELETE permissions to S3 Bucket
# * A CSV file with Item ARK key defined
# * S3 Bucket to modify
# * python3
# * pip3
# * pip3 install boto3
# 
# Example usage:
# python3 rename_ark.py -b test-iiif-cantaloupe-source -f test.csv
#
# If you want to override the default header key in the CSV:
# python3 rename_ark.py -b test-iiif-cantaloupe-source -f test.csv -k "OTHER ARK"
#################################################################################
import csv
import locale
import re
import boto3
import argparse

def strip_ark(ark_item):
  return re.sub("ark:/", "", ark_item)

def add_ark_prefix(ark_item):
  regex = re.compile("ark:/")
  if regex.search(ark_item):
    return ark_item
  else:
    return re.sub("^", "ark:/", ark_item)

def s3_object_exists(s3_key, s3_boto_conn, s3_bucket):
  try:
    resp = s3_boto_conn.get_object(Bucket=s3_bucket,Key=s3_key)
    if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
      return True
    else:
      return False
  except s3_boto_conn.exceptions.NoSuchKey:
    return False
  return False
 

def main():
  parser = argparse.ArgumentParser(description="S3 wrapper script to rename files with ark prefixes")
  parser.add_argument("-b", "--bucket", help="Bucket name associated with objects to modify", required=True)
  parser.add_argument("-f", "--file", help="CSV File to read", required=True)
  parser.add_argument("-k", "--key", help="The key of the CSV header to select for the source S3 object to rename")
  args = vars(parser.parse_args())

  conflict_list = []
  process_list = []
  client = boto3.client("s3")
  s3_bucket = args['bucket']
  with open(args['file'], "r", newline="") as f:
    r = csv.DictReader(f, delimiter=",")
    if args['key']:
      csv_key = args['key']
    else:
      csv_key = "Item ARK"
    image_suffix = ".jpx"
    for e in r:
      i = (strip_ark(e[csv_key]), add_ark_prefix(e[csv_key]))
      print("Processing %s:" % (i,))
      src_key = "%s%s" % (i[0], image_suffix)
      dest_key = "%s%s" % (i[1], image_suffix)
      s3_src_path = "%s/%s" % (s3_bucket, src_key)
      s3_dest_path = "%s/%s" % (s3_bucket, dest_key)
      # If the source bucket key does not exist, or if the destination key exists, skip this tuple and append a warning
      if not (s3_object_exists(src_key, client, s3_bucket)) or s3_object_exists(dest_key, client, s3_bucket):
        conflict_list.append(i)
      else:
        resp = client.copy_object(Bucket=s3_bucket, CopySource=s3_src_path, Key=dest_key)
        if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
          process_list.append(i)
          client.delete_object(Bucket=s3_bucket, Key=src_key)


    if conflict_list:
      print("The following objects have conflicts and were skipped:")
      for entry in conflict_list:
        print(entry)

    print("\nSuccessfully processed %d objects" % len(process_list))

if __name__ == "__main__":
  main()
