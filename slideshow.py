import asyncio, aiohttp, fake_useragent, builtins, bs4, pathlib

async def main():
    async with aiohttp.ClientSession(headers={'User-Agent':fake_useragent.UserAgent().chrome}, cookies={'AP_Login':'1', 'AP_Login_E':'1', 'AP_Force_logout':'1', 'AP_Username':'VnhWQnd4eG9GYzh0eCs2QXBYY1FKYk9RQjRNcUJlVTlQZmlGK1UyZmQyYz06OpwsmVc0JDqKHP%2F%2FDaOFP7k%3D'}) as client:
        CampaignId = '101687'
        async with client.post('https://timebucks.com//publishers/lib/scripts/api/BuyTasksUsersCampaigns.php', data={'action':'GetAllCampaigns'}) as advertiser:
            _ = await advertiser.json(content_type=None)
            Proof = builtins.next((_1.get('Proof') for _1 in _.get('Campaigns') + _.get('LazyCampaigns') if _1.get('Id') == CampaignId), '1')
        async with client.post('https://timebucks.com/publishers/lib/scripts/api/BuyTasksUsers.php', data={'g-recaptcha-response':'', 'CampaignId':CampaignId, 'action':'ValidateCaptcha'}) as _:pass
        async with client.post('https://timebucks.com/publishers/lib/scripts/api/BuyTasksUsersSubmission.php', data={'action':'ValidateTimeLimit', 'CampaignId':CampaignId}) as _:print(await _.json(content_type=None))
        async with client.get('https://timebucks.com/task_email_code.php') as code:
            with aiohttp.MultipartWriter('form-data') as multipart:
                multipart.append('SubmitUserTask').set_content_disposition('form-data', name='action')
                multipart.append(CampaignId).set_content_disposition('form-data', name='CampaignId')
                multipart.append(Proof).set_content_disposition('form-data', name='ProofType')
                multipart.append(bs4.BeautifulSoup(await code.text(), 'lxml').find('strong').string).set_content_disposition('form-data', name='Username')
                multipart.append(b'').set_content_disposition('form-data', name='SupportFiles', filename='')
                async with client.post('https://timebucks.com/publishers/lib/scripts/api/BuyTasksUsersSubmission.php', data=multipart) as _:print(_.url)
        async with client.post('https://timebucks.com/publishers/lib/scripts/api/BuyTasksUsers.php', data={'action':'CancelCampaign', 'CampaignId':CampaignId}) as _:pass
        async with client.get('https://timebucks.com/publishers/lib/scripts/php/action.php', params={'action':'getDailyPole'}) as getDailyPole:
            _ = await getDailyPole.json(content_type=None)
            if _.get('status') == 1: 
                pollQuestionID = _.get('pollQuestionID')
                answerID = builtins.next(builtins.iter(_.get('poll_options').keys()))
                async with client.post('https://timebucks.com/publishers/lib/scripts/php/action.php', data={'action':'submitDailyPole', 'answerID':answerID, 'pollQuestionID':pollQuestionID}) as submitDailyPole: print(await submitDailyPole.json(content_type=None))
        '''for _ in builtins.range(20):
            async with client.get('https://timebucks.com/publishers/lib/scripts/php/action_slideshows.php', params={'action':'viewTimecaveApiCall'}) as viewTimecaveApiCall:
                _ = (await viewTimecaveApiCall.json(content_type=None)).get('data')[0]
                clickUrl = _.get('click_url')
                termId = _.get('term_id')
                async with client.post('https://timebucks.com/publishers/lib/scripts/php/action_slideshows.php', data={'action':'AddSlideShowRefer', 'term_id':termId}) as AddSlideShowRefer:pass
                async with client.get(clickUrl) as _:print(_.url)
                await asyncio.sleep(20)
                for _ in builtins.range(2, 9):
                    async with client.get(clickUrl.replace('?', f'/page/{_}/?')) as _:print(_.url)
                    await asyncio.sleep(20)
                await asyncio.sleep(60 * 10)'''

asyncio.run(main())

#https://timebucks.com/redirects/PushClicks.php
'''curl 'https://timebucks.com/publishers/lib/scripts/php/action_clicks_verify.php' \
  -H 'authority: timebucks.com' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'cookie: timebucks_how_works_cave=1; ipqsd=206613528453328450; _aimtellSubscriberID=1c1b5673-5207-9de5-c1f6-d6216c0b8c48; browser_tid1=354303a5-9952-4f39-9974-97451bf9c1f6; hideouttv=222901118; intercom-device-id-cesrmnmn=59308379-3fff-42b4-a569-d17631d3be33; __stripe_mid=c572e1f2-5351-4845-a7ea-b51dca0aeeb96d75a7; device_id_1689277037=FGI77YS2IM-1689277037; device_id_1689983325=FTrJZkGFMl-1689983325; UTGv2=D-h461502889f7013dc2f6fe0f5e984e65b650; device_id_1691556638=Fy59rLCrSk-1691556638; AP_Login=1; AP_Login_E=1; AP_Force_logout=1; AP_Username=TFVEOU1GRGtqWjVoOVBGZHc3bHl0VXFhZmg3YzVZUVhVQ3Q4VWdadTdmTT06Oh0MOLTgFwYk%2BUiQZakS0vI%3D; _gid=GA1.2.478685933.1692949345; __stripe_sid=93e18aab-1eb0-457a-9807-5e0e01eb44a0cb2ea1; timebucks=2661edb7f08550f3a9aea6caa0617fb4; cf_clearance=FztHl2rnfZ6AXTJc6Jbgg7AADBdvDIRj2wjAs4eoYTE-1692972680-0-1-c1b45909.6213c3f6.4324cafc-0.2.1692972680; _ga=GA1.1.20369123.1688450607; tb_clicks_signature=4b61251c2c1c2e1ffa79059c51313378072d2bc2c899c6a0fbf0d42c2dadb253; tb_signature=a3553ac2b45b289cd377a6f1ae871f35c7fa4f8a004895ecdd502e971f4acc77; tb_usk=3e315953-2516-4585-a652-d9cc2f4ce9da; tb_logout=41b639a1ad8e83ced352d7fe38d7acacae6bb2f086933dc17bf0853618851775; _ga_PWLJ8BRHVD=GS1.1.1692949387.45.1.1692973362.0.0.0; intercom-session-cesrmnmn=ZTM0TDVDcVo2VkFBOXZDZU5KYURCdzQ3eXJiSEpZcmIxRG5yRG84amh4TDBWT3RDZll5QWRvbHhXZGJiWEJFby0tbTJjUGFuZnBSMHJvWHJXdVNiS3A4QT09--108750e1688398214492c989e389d613ff448851' \
  -H 'origin: https://timebucks.com' \
  -H 'pragma: no-cache' \
  -H 'referer: https://timebucks.com/redirects/PushClicks.php' \
  -H 'sec-ch-ua: "Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest' \
  --data-raw 'action=VerifyPushClicksCaptchaInstant&response=03ADUVZwAoqSeXt6xisNJJFMoVKDtExeREhx-vMN5BK9TUvJNEpE5Q15qZdZkh0HpgHllyXgc73sYo4oQC1sXeRi_iEdeVk_AK1S1oyRkk0HkRFBmMSblD1Bmsh0kl2iizzspl5K_b2q5VTZL3anMBBymQFupWFZLwZBWC86POGuIur2jmRTMe4otv-r0a9K1tQGvx-KaEFaxwGbZSW0uru1NyMFrqXga9aduO00p33g5bs5c4c-8ahpyU1S8ySXDb71SJoVVfKJR2Amc6KZZ6FsMOnE9ul9tXccniyudNgPFFjaLghzhfCPfDbzkM2nZD-8HCzRzZlBrcl0uonvVMyftZ0QHlCdDvy1mJaXrSkF3fVZjdvTGU3g3Opz-H-E_x85gvmAdT1ZWdGiYz9YENhnqZ178OzB4AF2T7fK-xQvkADGBfACI63zFGFohRiUnql7dLt1TcQwgeHTMx19VLaqRKTKi62oPG1XVhDWxGAV0NdmlHEjZXNondcvB-rgUfnX2OZ_nS5r3yYUuDrTHT61nHVckdF8L0I0vRXYf7o7OJFm0FRAqWiocxDX4a8HiQmumI4k1WuI6llK5xB3rpNJQFc2INJk-xJ0H3__Od0mefGteTiusF5Ej_Dp7hCj8UQdPzw5Q3eh7I&token=' \
  --compressed'''
