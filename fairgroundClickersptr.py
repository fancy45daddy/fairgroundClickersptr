import aiohttp, asyncio, bs4, fake_useragent, argparse, re, builtins, locale, sys
parser = argparse.ArgumentParser()
parser.add_argument('password')
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def check(_):
    return _.find(string='Invalid paid mail ID.') or _.find(string=re.compile('You have already visited this sponsor and')) or _.find(string=re.compile('Invalid paid mail ID - Ad Has Expired')) or _.find('b', string='Sorry, this link just expired')

async def pathnames(client, pathnames):
    hostname = pathnames[0].split('/')[2]
    for pathname in pathnames:
        flag = False
        while True:
            async with client.get(pathname) as page:
                pas = [_.get('href') for _ in bs4.BeautifulSoup(await page.text(), 'lxml').find_all('a', attrs={'href':re.compile('/scripts/runner\.php\?PA=')}) if 'cheatlink' not in _.find('img').get('src')]
                if flag or not pas: break
                for _ in pas:
                    async with client.get(_) as pa:
                        paHtml = bs4.BeautifulSoup(await pa.text(), 'lxml')
                        if paHtml.find('img', attrs={'src':'http://my-ptr.com/pages/botdetect_top.gif'}):
                            async with client.post(_, data={'q':paHtml.find('input', attrs={'name':'q'}).get('value'), 'a':'1', 'submit':'Continue >>'}) as _:paHtml = bs4.BeautifulSoup(await _.text(), 'lxml')
                        for keLink in paHtml.find_all('a', attrs={'href':re.compile('/scripts/runner\.php\?KE=')}):
                            print(pathname, keLink)
                            async with client.get(f'http://{hostname}{keLink.get("href")}') as ke:
                                print(ke.url)
                                keHtml = bs4.BeautifulSoup(await ke.text(), 'lxml')
                                if flag := sys.modules['__main__'].check(keHtml):
                                    fr = None
                                    break
                                elif (frTag := keHtml.find('frame', attrs={'src':re.compile('FR')})):
                                    fr = frTag.get('src')
                                    break
                        else:
                            if flag := sys.modules['__main__'].check(paHtml):continue
                            fr = None
                            try:
                                fr = paHtml.find('frame', attrs={'src':re.compile('FR')}).get('src')
                            except:
                                print(pathname, paHtml, _)
                                sys.exit(0)
                        if fr is None: continue
                        async with client.get(fr) as wait: await asyncio.sleep(builtins.int(re.search('(?<=\s)\d+(?=\s+seconds)', bs4.BeautifulSoup(await wait.text(), 'lxml').find(string=re.compile('seconds'))).group()))
                        async with client.get(fr) as balance: print(page.url, bs4.BeautifulSoup(await balance.text(), 'lxml').find_all(string=re.compile('cash|point', re.I)))

async def fairgroundClickersptr(hostname):
    async with aiohttp.ClientSession(headers={'user-agent':fake_useragent.UserAgent().chrome}, connector=aiohttp.TCPConnector(force_close=True)) as client:
        async with client.post(f'http://{hostname}/pages/enter.php', data={'username':'chaowen.guo1@gmail.com', 'password':parser.parse_args().password, 'submit':'Login'}) as enter:
            enterHtml = bs4.BeautifulSoup(await enter.text(), 'lxml')
            if hostname == 'clicksmania.net':
                async with client.get(f'http://{hostname}/pages/exchanger.php') as exchanger:
                    if points := bs4.BeautifulSoup(await exchanger.text(), 'lxml').find('th'):
                        async with client.post(f'http://{hostname}/pages/exchanger.php', data={'points':re.search('\d+', points.string).group(0), 'confirm':'exchange now'}) as _:pass
            elif hostname != 'email-moneymaker.com' and hostname != 'preciouspomsptr.com':
                link = enterHtml.find('a', attrs={'href':re.compile('cpconverter')}).get('href')
                async with client.get(link) as cpconverter:
                    cpconverterHtml = bs4.BeautifulSoup(await cpconverter.text(), 'lxml')
                    if (current := builtins.int(locale.atof(cpconverterHtml.find('b', string='Your Total Current Available Points: ').find_next('b').string))) > (min := builtins.int(cpconverterHtml.find('b', string='The Minimum Amount of Points to Convert for your member type is: ').find_next('b').string)):
                        min = min if min else 100
                        async with client.post(link, data={'points': (current // min) * min,'msg_mode':'Convert Now'}) as _: pass
            pathnames = [href for _ in enterHtml.find('b', string='Earn').find_next('table').find_all('a') if not (href := _.get('href')).endswith('inbox.php') and not href.endswith('upptc.php') and not href.endswith('uppoints.php') and not href.endswith('xxx.php') and not href.endswith('newsurfer_contests.php') and not href.endswith('newsurfer.php') and not href.endswith('ptpmain.php') and not href.endswith('special_membersarea2.php') and not href.endswith('xxx') and not href.endswith('adstatmaster.php') and not href.endswith('ptpapproved.php') and not href.endswith('tgbaffmain.php') and not href.endswith('perptcmain.php') and not href.endswith('hangman.php')]
            match hostname:
                case 'email-moneymaker.com': pathnames = [f'pages/{_}' for _ in ('ptc', 'kwikkieptc', 'ptsearch', 'pointcptc', 'serenity')]
                case 'clicksmania.net': pathnames = [f'pages/{_}' for _ in ('treasure', 'ptc_cash_ptc', 'ptsearch1', 'mania', 'tgbtrroom', 'pointcptc', 'ptc-points')]
                case 'preciouspomsptr.com': pathnames = [f'pages/{_}' for _ in ('ptsearch', 'ptc', 'ptcontent', 'game', 'treasure', 'pointsptc')]
            async with client.get(enterHtml.find('a', attrs={'href':re.compile('tgbaffmain')}).get('href')) as tgbaffmain:
                regex = re.compile(f'{hostname}/(\w+)\.php\?refid=\\1')
                pathnames += (_.get('href') for _ in bs4.BeautifulSoup(await tgbaffmain.text(), 'lxml').find_all('a', attrs={'href':regex}))
            async with client.get(enterHtml.find('a', attrs={'href':re.compile('perptcmain')}).get('href')) as perptcmain:
                regex = re.compile(f'{hostname}/(\w+)ptc(c|p)\.php\?refid=\\1')
                pathnames += (_.get('href') for _ in bs4.BeautifulSoup(await perptcmain.text(), 'lxml').find_all('a', attrs={'href':regex}))
            await sys.modules['__main__'].pathnames(client, pathnames)

async def polarbearclicks(hostname):
    async with aiohttp.ClientSession(headers={'user-agent':fake_useragent.UserAgent().chrome}, connector=aiohttp.TCPConnector(force_close=True)) as client:
        async with client.post(f'http://{hostname}/pages/enter.php', data={'username':'chaowen.guo1@gmail.com', 'password':parser.parse_args().password, 'submit':'Login'}) as enter:
            enterHtml = bs4.BeautifulSoup(await enter.text(), 'lxml')
            if hostname == 'wallabymail.info': pathnames = ['http://wallabymail.info/pages/ptc.php', 'http://wallabymail.info/pages/ptc_contest.php']
            else: pathnames = [href for _ in enterHtml.find('font', string='Ways To Earn').find_all_next('a', limit=16) if not (href := _.get('href')).endswith('inbox.php') and not href.endswith('xxx.php') and not href.endswith('special_membersarea2.php') and not href.endswith('redeem.php') and not href.endswith('upgraded.php') and not href.endswith('cancel_account.php') and not href.endswith('ptpmain.php') and not href.endswith('autosurf1.php') and not href.endswith('withdraw.php') and not href.endswith('userinfo.php') and not href.endswith('climb_toplist.php')]
            async with client.get(enterHtml.find('a', attrs={'href':re.compile('tgbaffmain')}).get('href')) as tgbaffmain:
                regex = re.compile(f'{hostname}/(\w+)\.php\?refid=\\1')
                pathnames += (_.get('href') for _ in bs4.BeautifulSoup(await tgbaffmain.text(), 'lxml').find_all('a', attrs={'href':regex}))
            async with client.get(enterHtml.find('a', attrs={'href':re.compile('perptcmain')}).get('href')) as perptcmain:
                regex = re.compile(f'{hostname}/(\w+)ptc(c|p)\.php\?refid=\\1')
                pathnames += (_.get('href') for _ in bs4.BeautifulSoup(await perptcmain.text(), 'lxml').find_all('a', attrs={'href':regex}))
            await sys.modules['__main__'].pathnames(client, pathnames)

'''case 'email-moneymaker.com': pathnames = [f'pages/{_}' for _ in ('ptc', 'kwikkieptc', 'ptsearch', 'pointcptc', 'serenity')]
case 'clicksmania.net': pathnames = [f'pages/{_}' for _ in ('treasure', 'ptc_cash_ptc', 'ptsearch1', 'mania', 'tgbtrroom', 'pointcptc', 'ptc-points')]
case 'preciouspomsptr.com': pathnames = [f'pages/{_}' for _ in ('ptsearch', 'ptc', 'ptcontest', 'game', 'treasure', 'pointsptc')]
case 'infofriendptr.com': pathnames = [f'pages/{_}' for _ in ('tgbtrroom', 'ptc', 'ptcontest', 'ptsearch', 'treasure', 'pointptc')]'''

async def guardianmails(hostname):
    async with aiohttp.ClientSession(headers={'user-agent':fake_useragent.UserAgent().chrome}, connector=aiohttp.TCPConnector(force_close=True)) as client:
        async with client.post(f'http://{hostname}/pages/enter.php', data={'username':'chaowen.guo1@gmail.com', 'password':parser.parse_args().password, 'submit':'Login'}) as enter:
            enterHtml = bs4.BeautifulSoup(await enter.text(), 'lxml')
            pathnames = [href for _ in enterHtml.find('font', string='Ways To Earn').find_all_next('a', limit=8) if not (href := _.get('href')).endswith('inbox.php') and not href.endswith('newsurfer.php') and not href.endswith('ptpmain.php') and not href.endswith('sinnyaffmain.php')]
            if hostname == 'my-ptr.com': pathnames = ['http://www.my-ptr.com/pages/sub_ptc.php' if _ == 'http://www.my-ptr.com/pages/ptc.php' else _ for _ in pathnames]
            async with client.get(enterHtml.find('a', attrs={'href':re.compile('sinnyaffmain')}).get('href')) as sinnyaffmain: pathnames += (''.join(('http://', hostname, _.get('href'))) for _ in bs4.BeautifulSoup(await sinnyaffmain.text(), 'lxml').find_all('a', attrs={'class':'fill_div'}))
            await sys.modules['__main__'].pathnames(client, pathnames)

async def main():
    #await asyncio.gather(*(fairgroundClickersptr(_) for _ in ('billiondollarmails.com', 'fairground-clickersptr.com', 'myster-e-mail.com', 'www.roadto51.com', 'www.homesteadmails.com', 'payingemails4u.com', 'butterfliesnroses.com', 'classicalmails.com', 'email-moneymaker.com', 'clicksmania.net')), *(guardianmails(_) for _ in ('dreammails.net', 'bluerosepost.com', 'hot-rods-ptr.com', 'my-ptr.com')))
    await asyncio.gather(*(fairgroundClickersptr(_) for _ in ('billiondollarmails.com', 'fairground-clickersptr.com', 'myster-e-mail.com', 'roadto51.com', 'homesteadmails.com', 'payingemails4u.com', 'butterfliesnroses.com', 'classicalmails.com')), *(polarbearclicks(_) for _ in ('circlecptr.com', 'polarbearclicks.com', 'aftermidnightmails.info', 'wallabymail.info')), guardianmails('my-ptr.com'))

asyncio.run(main())
