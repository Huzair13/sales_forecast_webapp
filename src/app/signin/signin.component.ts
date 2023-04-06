import { Component } from '@angular/core';


@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})
export class SigninComponent {
  submit() {
    // Handle form submission here
  }
  onFileSelected(event: any) {
    // handle file upload here
  }

  getForecast() {
    // handle getting forecast here
  }
}
