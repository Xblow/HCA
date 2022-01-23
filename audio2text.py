from deepgram import Deepgram
import asyncio, json
import argparse


async def dg(url: str):
    # Initializes the Deepgram SDK
    dg_client = Deepgram(APIKEY_DEEPGRAM)

    source = {'url': url}
    response = await dg_client.transcription.prerecorded(source,  {'punctuate': True})
    # print(type(response))
    output = response["results"]["channels"][0]["alternatives"][0]["transcript"]
    # print(type(output))
    return output


def get_transcript(url='') -> str:
    """
    Get transcript from audio using Deepgram services
    """
    if not url:
        print('Using sample url')
        url = 'https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav'
    return asyncio.run(dg(url))

