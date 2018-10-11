This directory contains everything required to extract the submission matrices for all (training) courses in the MORF repository.

Build the docker image with

```
docker build -f dockerfile .
```

and use `docker save` to save the file to a .tar. This will require the unique container ID provided at the end of the `docker build` output.

Then, put the docker image somewhere public (i.e., a public S3 bucket or https location) and submit to MORF using the MORF API functions.

More information about submitting to MORF is available here: https://educational-technology-collective.github.io/morf/getting-started/


