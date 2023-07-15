export interface Settings {
  vimMode: boolean
  theme: string
  font: string
}

export class AppSettings {

  vimMode: boolean = false
  theme: string = "materialDark"
  font: string = "SpaceMono"

  constructor() {
    if (localStorage.getItem("sardine_settings") !== null) {
      let settings = JSON.parse(localStorage.getItem("sardine_settings") as string)
      this.vimMode = settings.vimMode
      this.theme = settings.theme
      this.font = settings.font
    } else {
      localStorage.setItem("sardine_settings", JSON.stringify(this))
    }
  }

  get data(): Settings {
    return {
      vimMode: this.vimMode,
      theme: this.theme,
      font: this.font
    }
  }
}