import sys

from dffml import *

from dffml_operations_us_reps.oregon import *


class TestOregon(AsyncTestCase):
    async def test_orgeon(self):
        self.maxDiff = None
        dataflow = DataFlow.auto(or_address_to_cords, or_find_reps, GetSingle)
        check = {
            "1221 SW 4th Ave, Portland, US 97204": {
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
                        value=[or_find_reps.op.outputs["result"].name,],
                        definition=GetSingle.op.inputs["spec"],
                    ),
                ]
                for key in check.keys()
            },
        ):
            ctx_str = (await ctx.handle()).as_string()
            self.assertDictEqual(check[ctx_str], results)
