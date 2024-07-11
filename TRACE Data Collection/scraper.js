const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
const { isStringObject } = require('util/types');
var username = "li.vi";
var password = "BlueEagle123!";

// mod, scim, ibs, eANDi, accounting, marketing done
var names_reversed = ['Gillani, Nabeel', 'Grinstein, Amir', 'Johnson, Brooke', 'Shichor, Karlinsky, Yael', 'Keeney, Ashley', 'Knight, Samsun', 'Kumar, Smriti', 'Kurt, Didem', 'Lassk, Felicia', 'Lee, Shun-Yang', 'Lefevre, Duane', 'Matherly, Ted', 'Mathras, Daniele', 'Mauristhene, Ernest', 'McCullough, Robert', 'Mulki, Jay', "O'Connor, Chad", 'Pauwels, Koen', 'Pei, Amy', 'Rivas, Ron', 'Rocklage, Matt', 'Runge, Julian', 'Sands, Erica', 'Sieloff, Jeffrey', 'Steffel, Mary', 'Stewart, Rachel', 'Sultan, Fareena', 'Thomas, Sharon', 'Weaver, Ray', 'Yadin, Dena', 'Yencho, Jennifer', 'Yin, Yi'];
var names = ['Nabeel, Gillani', 'Amir, Grinstein', 'Brooke, Johnson', 'Yael, Karlinsky, Shichor', 'Ashley, Keeney', 'Samsun, Knight', 'Smriti, Kumar', 'Didem, Kurt', 'Felicia, Lassk', 'Shun-Yang, Lee', 'Duane, Lefevre', 'Ted, Matherly', 'Daniele, Mathras', 'Ernest, Mauristhene', 'Robert, McCullough', 'Jay, Mulki', "Chad, O'Connor", 'Koen, Pauwels', 'Amy, Pei', 'Ron, Rivas', 'Matt, Rocklage', 'Julian, Runge', 'Erica, Sands', 'Jeffrey, Sieloff', 'Mary, Steffel', 'Rachel, Stewart', 'Fareena, Sultan', 'Sharon, Thomas', 'Ray, Weaver', 'Dena, Yadin', 'Jennifer, Yencho', 'Yi, Yin'];
var neu_login = "https://www.applyweb.com/eval/shibboleth/neu/36892"

function sleep(ms) {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  }

function isFall2023(entry) {
  const text = entry[0];
  if (typeof text === 'string') {
    return text.includes('Fall') && text.includes('2023');
  }
  return false
}

async function getFall2023Links(frame2) {
  linksText = await frame2.evaluate(() => Array.from(document.querySelectorAll('#resultTable > tbody > tr'), element => element.textContent));
  links = await frame2.evaluate(() => Array.from(document.querySelectorAll('#resultTable > tbody > tr > td:nth-child(6) > a'), element => element.href));
  links = linksText.map((x,i) => [x, links[i]]);
  links = links.filter(isFall2023);
  links = links.map(e => e[1]);
  return links;
}

function checkExistsWithTimeout(filePath, timeout) {
  return new Promise(function (resolve, reject) {

      var timer = setTimeout(function () {
          watcher.close();
          reject(new Error('File did not exists and was not created during the timeout.'));
      }, timeout);

      fs.access(filePath, fs.constants.R_OK, function (err) {
          if (!err) {
              clearTimeout(timer);
              watcher.close();
              resolve();
          }
      });

      var dir = path.dirname(filePath);
      var basename = path.basename(filePath);
      var watcher = fs.watch(dir, function (eventType, filename) {
          if (eventType === 'rename' && filename === basename) {
              clearTimeout(timer);
              watcher.close();
              resolve();
          }
      });
  });
}

(async () => {
    // browser and page set up
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    page.setViewport({ width: 1366, height: 768});

    // login to NU
    await page.goto(neu_login);
    await page.waitForNavigation();
    await page.type('input[name=j_username]', username);
    await page.type('input[name=j_password]', password);
    await page.evaluate(() => {
        document.querySelector('button[type=submit]').click();
    });
    await page.waitForNavigation();

    // wait for DUO, then press on the push notification button
    await sleep(5000);
    const f = await page.$("iframe[id='duo_iframe']");
    const frame = await f.contentFrame(); // wait for iframe
    const [button] = await frame.$x("//button[contains(., 'Send Me a Push')]");
    if (button) {
        await button.click();
    }

    // NEED TO CONFIRM on mobile
    await sleep(20000);

    // iterate through all professors
    for (let n = 0; n < names.length; n++) {
      const prof_name_space = names[n];
      const prof_name = names[n].replace(',', '').replace(' ', '_');
      const prof_reversed_name = names_reversed[n];
      console.log("on", prof_name_space);

      // set the download path to the folder of the professor's name
      await page._client().send('Page.setDownloadBehavior', {behavior: 'allow', downloadPath: path.resolve(__dirname, prof_name)});
      
      // go to report browser, then wait for everything to load
      await page.goto('https://www.applyweb.com/eval/new/reportbrowser');
      await sleep(3000);
      const f2 = await page.$('iframe[id="contentFrame"]');
      const frame2 = await f2.contentFrame();
      await sleep(5000);
      
      // type in the name and search
      await frame2.type('input[ng-model="search"]', prof_name_space); 
      const [search] = await frame2.$x("//button[contains(., 'Go')]");
      if (search) {
          await search.click();
      }

      // wait for entries to load
      await sleep(5000);
      var links = []

      // if there isn't a view all, get the links on the page, if there arent any, try reversed name
      let isViewAll = (await frame2.$('#tapestryContainer > div > div:nth-child(1) > div.col-sm-12 > form > a')) || "";
      if (isViewAll == "") {
        try {
          links = await getFall2023Links(frame2);
          if (links.length > 0) {
            console.log('no view all button, but have links', links);
          }
        } catch {
          console.log('no view all button, and no links');
        }
      } else {
        await frame2.click('#tapestryContainer > div > div:nth-child(1) > div.col-sm-12 > form > a');
        // click yes, in view all pop-up
        const [yes] = await frame2.$x("//button[contains(., 'Yes')]");
        if (yes) {
            await yes.click();
        }
        await sleep(10000);
        links = await getFall2023Links(frame2);
      }

      // try the name reversed
      if (links.length == 0) {
        console.log('trying name, reversed');
        // try second name
        await frame2.click('input[ng-model="search"]',{ clickCount: 3 });
        await frame2.type('input[ng-model="search"]', prof_reversed_name); 
        const [search] = await frame2.$x("//button[contains(., 'Go')]");
        if (search) {
          await search.click();
        }
        // wait for entries to load
        await sleep(10000);

        // run same logic
        let isViewAll = (await frame2.$('#tapestryContainer > div > div:nth-child(1) > div.col-sm-12 > form > a')) || "";
        if (isViewAll == "") {
          try {
            links = await getFall2023Links(frame2);
            if (links.length > 0) {
              console.log('no view all button, but have links', links);
            }
          } catch {
            console.log('no view all button, and no links');
          }
        } else {
          await frame2.click('#tapestryContainer > div > div:nth-child(1) > div.col-sm-12 > form > a');
          // click yes, in view all pop-up
          const [yes] = await frame2.$x("//button[contains(., 'Yes')]");
          if (yes) {
              await yes.click();
          }
          await sleep(10000);
          links = await getFall2023Links(frame2);
        }
      }
      if (links.length == 0) {
        console.log('no links found');
      }

      console.log(links);
      // go to every link
      for (var i = 0; i < links.length; i++) {
        try {
          await page.goto(links[i]);
          await sleep(1500);
          const f = await page.$('iframe[id="contentFrame"]');
          const frame = await f.contentFrame();
          
          // course title 
          var title = await frame.$eval('#tapestryContainer > div.container-fluid > div:nth-child(3) > div > div > div.col-xs-6.text-left > ul > li:nth-child(3) > strong', el => el.textContent);
          // course section
          var section = await frame.$eval('#tapestryContainer > div.container-fluid > div:nth-child(3) > div > div > div.col-xs-6.text-left > ul > li:nth-child(2) > strong', el => el.textContent);
          // course id
          var courseid = await frame.$eval('#tapestryContainer > div.container-fluid > div:nth-child(3) > div > div > div.col-xs-6.text-left > ul > li:nth-child(4) > strong', el => el.textContent);
          // semester
          var semester = await frame.$eval('#tapestryContainer > div.container-fluid > div:nth-child(3) > div > h3', el => el.textContent);
          var semester_substring = semester.substring(
            semester.indexOf("(") + 1, 
            semester.lastIndexOf(")")
          );
          var filename = title + " " + semester_substring + " " + section + " " + courseid;
          filename = filename.split(' ').join('_').replace('/', '_').replace('\\', '_').replace('|', '_').replace(':','');

          // make folder if first time
          if (i == 0 && !fs.existsSync('./' + prof_name)) {
            fs.mkdirSync('./' + prof_name);
          }
          
          // download the xls
          await frame.click('#tapestryContainer > div.container-fluid > div.pull-right > a:nth-child(2)');
          console.log('downloading...')

          // rename the file when the original is done downloading, timeout is 20s
          await checkExistsWithTimeout(path.resolve(__dirname, prof_name) + '/quantitative_report.xls', 120000);
          fs.rename(path.resolve(__dirname, prof_name) + '/quantitative_report.xls', path.resolve(__dirname, prof_name) + '/' + filename + '.xls', () => {
            console.log('renamed to:', path.resolve(__dirname, prof_name) + '/' + filename + '.xls');});
          
          console.log('downloaded', i + 1)
        } catch (error) {
          i = i - 1;
          console.log('failed, trying again', error);
        }
      }
    }
    await browser.close();
})();

