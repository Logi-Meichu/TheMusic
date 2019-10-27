import QtQuick 2.0
import MuseScore 3.0

MuseScore {
      menuPath: "Plugins.transpose-down"
      description: "Description goes here"
      version: "1.0"
      onRun: {
            cmd("transpose-down")
            Qt.quit()
            }
      }