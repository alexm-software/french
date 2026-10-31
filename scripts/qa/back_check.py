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
    print('ok',ok,'/',len(CASES),'js errors',errs)
    await b.close()
asyncio.run(main())
