import sys

from dffml import *

from dffml_operations_us_reps.oregon import *


class TestOregon(AsyncTestCase):
    async def test_orgeon(self):
        dataflow = DataFlow.auto(or_address_to_cords, or_find_reps, GetSingle)
        check = {
            "1221 SW 4th Ave, Portland, US 97204": {
                or_address_to_cords.op.outputs["result"].name: {
                    "x_y": {"x": -13656574.330719888, "y": 5702952.187275884},
                    "x_y_min_max": {
                        "xmin": -13656685.650210682,
                        "ymin": 5702793.325050546,
                        "xmax": -13656463.011229094,
                        "ymax": 5703111.0523242075,
                    },
                    "lat_lng": {"lat": 45.514917, "lng": -122.67909449999999},
                },
                or_find_reps.op.outputs["result"].name: {
                    "Representative Akasha Lawrence Spence": "Rep.AkashaLawrenceSpence@oregonlegislature.gov",
                    "Senator Ginny Burdick": "Sen.GinnyBurdick@oregonlegislature.gov",
                },
            }
        }
        async for ctx, results in run(
            dataflow,
            {
                key: [
                    Input(
                        value=key,
                        definition=or_address_to_cords.op.inputs["address"],
                    ),
                    Input(
                        value=[
                            or_address_to_cords.op.outputs["result"].name,
                            or_find_reps.op.outputs["result"].name,
                        ],
                        definition=GetSingle.op.inputs["spec"],
                    ),
                ]
                for key in check.keys()
            },
        ):
            ctx_str = (await ctx.handle()).as_string()
            self.assertDictEqual(check[ctx_str], results)
