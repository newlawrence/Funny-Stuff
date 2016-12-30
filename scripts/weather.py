#!/usr/bin/env python3
# This script gathers all the thermal data files from https://energyplus.net
# Copyright (c) 2016 by Alberto Lorenzo - https://opensource.org/licenses/MIT

from functools import partial, reduce
import asyncio
from os import makedirs
from time import time

from aiofiles import open as aopen
from aiohttp import request
from lxml import html

base_link = html.fromstring('<a href="/weather">weather</a>')
base_url = 'https://energyplus.net'
toplevel = 3
repeated_levels = ['CAN - Canada', 'USA - USA']
file_extension = '.epw'
parallel_downloads = 100


def progress(curr=0, sav=0, prog=0., secs=0, end=False):
    total_cols = 10
    cols = int(total_cols * prog)
    end = '\n' if end else '\r'

    print(
        '[{c:<{tc}}]  {f:d} files  {d:d} MB  {p:d} %  time: {m:02d}:{s:02d}'
        .format(
            c='#' * cols,
            tc=total_cols,
            d=sav // 1048576,
            f=curr,
            p=int(prog * 100),
            m=secs // 60,
            s=secs % 60
        ),
        end=end
    )


async def get(*args, **kwargs):
    response = await request('GET', *args, **kwargs)
    return (await response.read())


async def download(url, path):
    async with aopen(path, 'wb') as file:
        content = await get(url)
        await file.write(content)
    return len(content)


async def harvest_links(link, base_path='.', level=toplevel):
    url = base_url + link.attrib['href']
    path = base_path + '/' + link.text

    if level > 0:
        page = html.fromstring(await get(url))
        links = page.find_class('btn-group-vertical')
        links = reduce(lambda x, y: x.extend(y) or x, links)
        makedirs(path, exist_ok=True)

        loop = asyncio.get_event_loop()
        tasks = []
        level = level - 1 if link.text not in repeated_levels else level
        for link in links:
            tasks.append(
                loop.create_task(
                    harvest_links(link, path, level)
                )
            )
        files = await asyncio.gather(*tasks)
        return {k: v for d in files for k, v in d.items()}

    else:
        url = url.replace('location', 'download')
        url += url[url.rfind('/'):] + file_extension
        path += file_extension
        return {path: url}


def next_file(files, stat):
    path, url = files.popitem()
    task = loop.create_task(download(url, path))
    task.add_done_callback(
        partial(process_next, files=files, stat=stat)
    )
    return task


def process_next(future, files, stat):
    if files:
        next_file(files, stat)
    else:
        stat['tail'] += 1

    if stat['tail'] == parallel_downloads:
        loop = asyncio.get_event_loop()
        loop.stop()

    stat['curr'] += 1
    stat['prog'] = stat['curr'] / stat['files']
    stat['sav'] += int(future.result())
    stat['secs'] = int(time() - stat['start'])
    progress(stat['curr'], stat['sav'], stat['prog'], stat['secs'])

if __name__ == '__main__':
    print('Retrieving weather data files from {}'.format(base_url))
    print('Collecting download links...')
    loop = asyncio.get_event_loop()
    files = loop.run_until_complete(harvest_links(base_link))

    stat = {
        'tail': 0,
        'curr': 0,
        'prog': 0.,
        'sav': 0,
        'secs': 0,
        'start': time(),
        'files': len(files)
    }
    print('Downloading {} files...'.format(stat['files']))

    progress()
    for _ in range(parallel_downloads):
        next_file(files, stat)
    loop.run_forever()

    progress(stat['files'], stat['sav'], stat['prog'], stat['secs'], end=True)
    loop.close()
    print('Process complete!')
