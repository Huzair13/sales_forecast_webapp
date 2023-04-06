import { Component,Input,OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit{
  fileToUpload: File | null = null;

  jsonData: any;
  imageSrc: SafeUrl='';
  imageSrc2: SafeUrl='';
  selectedOption: any;

  condition = false;
  isLoading = false;

  durationInSeconds = 3;


  number: number=0;


  constructor(private http: HttpClient,private sanitizer: DomSanitizer,
    private router: Router,private authService: AuthService,private _snackBar: MatSnackBar) {}

//   const menuToggle = document.getElementById('menu-toggle');
// const navLinks = document.querySelector('.nav-links');
// // 
// menuToggle.addEventListener('click'), () => {
//   navLinks.classList.toggle('show');
// });

  ngOnInit(): void {
    window.addEventListener('unload', () => {
      sessionStorage.clear();
    });
  }

  goToNextPage() {
    const nextState = { data: 'some data' };
    window.history.pushState(nextState, '', '/next-page');
  }


  onFileSelect(event: any) {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.fileToUpload = file;
    }
  }

  onSubmit() {
    
    this.isLoading=true;
    const data = { selectedOption: this.selectedOption };

    const formData = new FormData();
    
    if (this.fileToUpload) {

      formData.append('file', this.fileToUpload, this.fileToUpload.name,);
      formData.append('number', this.number.toString());
      formData.append('selectedOption', this.selectedOption);

      this.http.post('http://localhost:5000/api/salesforecast', formData).subscribe(
        (res) => {
          this.jsonData = res;
          console.log(this.jsonData.data);
          this.imageSrc = this.sanitizer.bypassSecurityTrustUrl('data:image/png;base64,' + this.jsonData.image);
          this.imageSrc2 = this.sanitizer.bypassSecurityTrustUrl('data:image/png;base64,' + this.jsonData.image2);
          this.condition=true;
          this.isLoading=false;
          this._snackBar.open('Predicted ', 'Close', {
            duration: 3000,
            verticalPosition: 'bottom',
            horizontalPosition: 'left'
          });
        },
        (err) => {
          console.log(err);
        }
      );
    }
  }

  onDownload(){
    this.isLoading=true;
    this.http.post('http://localhost:5000/api/download_prediction', this.jsonData.data,{ responseType: 'blob' }).subscribe(
        (res) => {
          const blob = new Blob([res], { type: 'text/csv' });
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'data.csv';
          a.click();
          this.isLoading=false;
        },
        (err) => {
          console.log(err);
        }
      );
  }


  onLogout() {
    this.isLoading=true
    const url = 'http://localhost:5000/api/logout';
    this.http.delete(url).subscribe(
      (response: any) => {
        this.router.navigate([''],{ skipLocationChange: true });
        this.isLoading=false;
      },
      error => {
        console.log(error);
      }
    );
  }

}
