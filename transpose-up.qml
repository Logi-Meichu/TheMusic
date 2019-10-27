import QtQuick 2.0
import MuseScore 3.0

MuseScore {
      menuPath: "Plugins.transpose-up"
      description: "Description goes here"
      version: "1.0"
      onRun: {
            cmd("transpose-up")
            Qt.quit()
            }
      }
