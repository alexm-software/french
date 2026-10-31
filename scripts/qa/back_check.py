import asyncio
from playwright.async_api import async_playwright
CASES=[('kiosque/potins','#/quartier/'),('kiosque','#/quartier/'),('kiosque/redaction','#/quartier/'),('conservatoire/chorale','#/quartier/'),
('st_souffle/coiffeur','#/st_souffle'),('st_souffle','#/quartier/'),('cafe/comptoir','#/cafe/bar'),('cabinet/plateau','#/cabinet/docteur')]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    ok=0
    # walk via door first: kiosque -> potins, then Back must go to map not kiosque
    await pg.goto('http://localhost:8894/#/kiosque'); await pg.wait_for_timeout(1200)
    await pg.goto('http://localhost:8894/#/kiosque/potins'); await pg.wait_for_timeout(1200)
    await pg.click('#back'); await pg.wait_for_timeout(500); h=await pg.evaluate('location.hash'); print('walk kiosque->potins, Back ->',h, 'OK' if h.startswith('#/quartier/') else 'FAIL')
    for r,want in CASES:
      await pg.goto('http://localhost:8894/#/'+r); await pg.wait_for_timeout(1200)
      lab=await pg.evaluate("document.querySelector('#backLabel').textContent")
      await pg.click('#back'); await pg.wait_for_timeout(500); h=await pg.evaluate('location.hash')
      good=h.startswith(want) if want.endswith('/') else h==want
      ok+=good; print(r,'->',h,'['+lab+']','OK' if good else 'FAIL')
    # ⌂ Hub: second strip button -> first room / hub of the building or area; hidden in the hub itself (gate 19)
    HUB=[('kiosque/potins','#/kiosque'),('kiosque/radio','#/kiosque'),('conservatoire/chorale','#/conservatoire'),('st_souffle/coiffeur','#/st_souffle'),('cafe/comptoir','#/cafe'),('kiosque',None),('st_souffle',None)]
    for r,want in HUB:
      await pg.goto('http://localhost:8894/#/'+r); await pg.wait_for_timeout(1000)
      vis=await pg.evaluate("!document.querySelector('#hub').hidden && document.querySelector('#hub').offsetWidth>0")
      if want is None:
        good=not vis; print('hub',r,'hidden' if good else 'SHOWN in hub','OK' if good else 'FAIL')
      else:
        tip=await pg.evaluate("document.querySelector('#hub').title")
        if vis: await pg.click('#hub'); await pg.wait_for_timeout(500)
        h=await pg.evaluate('location.hash'); good=vis and h==want and bool(tip)
        print('hub',r,'->',h,'['+tip+']','OK' if good else 'FAIL')
      ok+=good
    await pg.goto('http://localhost:8894/#/'); await pg.wait_for_timeout(800)
    mh=await pg.evaluate("document.querySelector('#hub').hidden"); ok+=mh; print('hub hidden on map','OK' if mh else 'FAIL')
    print('ok',ok,'/',len(CASES)+len(HUB)+1,'js errors',errs)
    await b.close()
asyncio.run(main())
