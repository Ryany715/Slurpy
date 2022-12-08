const { SlippiGame } = require("@slippi/slippi-js");
const fs = require('fs');

function json_convert(filepath) {
  let input_folder = filepath
  if (fs.existsSync('json/')) {
    let output_folder = 'json/'
  } else {
    fs.mkdir('json/', err => {
      if (err) {
        throw err
      }
    })
    let output_folder = 'json/'
  }
  let directoryPath = input_folder
  fs.readdir(directoryPath, function (err, files) {
    //handling error
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    } 
    //listing all files using forEach
    files.forEach(function (file) {
        // Do whatever you want to do with the file
        //console.log(file); 
        let file_sub = file.substring(0,20)
        const game = new SlippiGame(input_folder + file);
        const settings = game.getSettings();
        const metadata = game.getMetadata();
        const stats = game.getStats();
        console.log(stats['overall']);
        let new_json = {'settings': settings,'metadata':metadata,'stats':stats};
        let stats_string = JSON.stringify(new_json);
        fs.writeFileSync(output_folder + file_sub + '.json', stats_string, err => {
            if (err) {
              console.error(err);
            }
            // file written successfully
          });

    });
  });
}

