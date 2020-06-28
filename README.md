# DFFML Operations for geting information on US representatives

## Usage

```console
$ dffml dataflow create usreps.or_address_to_cords usreps.or_find_reps get_single |
  dffml dataflow run records all \
    -record-def usreps.or_address_to_cords.inputs.address \
    -inputs usreps.or_find_reps.outputs.result,=get_single_spec \
    -configloader json \
    -dataflow /dev/stdin \
    -sources m=memory \
    -source-records '1221 SW 4th Ave, Portland, US 97204'
[
    {
        "extra": {},
        "features": {
            "usreps.or_find_reps.outputs.result": {
                "Representative Akasha Lawrence Spence": "Rep.AkashaLawrenceSpence@oregonlegislature.gov",
                "Senator Ginny Burdick": "Sen.GinnyBurdick@oregonlegislature.gov"
            }
        },
        "key": "1221 SW 4th Ave, Portland, US 97204",
        "last_updated": "2020-06-26T07:50:45Z"
    }
]
```

## HTTP Deployment DataFlow

```console
$ dffml dataflow create \
    usreps.or_address_to_cords \
    usreps.or_find_reps \
    get_single \
  -seed \
    usreps.or_find_reps.outputs.result,usreps.or_address_to_cords.outputs.result=get_single_spec \
  -configloader yaml |
  tee dffml_operations_us_reps/deploy/df/reps.yaml
```

## License

DFFML dffml-operations-us-reps is distributed under the [MIT License](LICENSE).
