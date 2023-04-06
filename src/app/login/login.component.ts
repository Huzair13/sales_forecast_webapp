import { Component, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { FormControl, Validators } from '@angular/forms';
import { AuthService } from '../auth.service';
import { ElementRef, Renderer2 } from '@angular/core';
import {MatSnackBar} from '@angular/material/snack-bar';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],

})
export class LoginComponent implements OnInit{

  hide: boolean = true;
  showSpinner = false;
  isLoading = false;
  uname: string = '';
  password : string='';
  errorMessage: string=''; 
  isLogin: boolean = true;

  //signUp initialization
  sp_uname:string='';
  sp_email:string='';
  sp_pass1:string='';
  sp_pass2:string='';
  
  semail:string='';
  spass:string='';
  suname:string='';
  srpass:string='';

  isSignInTabSelected: boolean = true;

  @ViewChild('sign_name_field') sign_name_field!: ElementRef;
  @ViewChild('sign_email_field') sign_email_field!:ElementRef;
  @ViewChild('sign_pass_field') sign_pass_field!:ElementRef;
  @ViewChild('sign_pass_re_field') sign_pass_re_field!:ElementRef;
  @ViewChild('log_name_field') log_name_field !:ElementRef;
  @ViewChild('log_pass_field') log_pass_field !:ElementRef;

  
  constructor(private http: HttpClient,private router: Router,
    private authService: AuthService,private elRef: ElementRef, 
    private renderer: Renderer2,private elementRef: ElementRef,private _snackBar: MatSnackBar) {}

  ngOnInit(): void {
    if (!localStorage.getItem('isLoggedIn')) {      
      this.router.navigate(['/login']);
    }
  }

  ngAfterViewInit(): void {
    const btn = document.querySelector('.btn') as HTMLElement;
    const btn2 = document.querySelector('.btn2') as HTMLElement;
    const card = document.querySelector('.card__inner') as HTMLElement;
    btn.addEventListener('click', (e: MouseEvent) => {
      card.classList.toggle('is-flipped');
    });
    btn2.addEventListener('click', (e: MouseEvent) => {
      card.classList.toggle('is-flipped');
    });

  }


  onFocus(event: Event) {
    const prevIcon = (event.target as HTMLElement).previousElementSibling;
    this.renderer.addClass(prevIcon, 'glowIcon');
  }

  onBlur(event: Event) {
    const prevIcon = (event.target as HTMLElement).previousElementSibling;
    this.renderer.removeClass(prevIcon, 'glowIcon');
  }


  toggleForm(): void {
    this.isLogin = !this.isLogin;
  }

  onSubmit1(){
    
    const uname1=this.uname;
    const password1=this.password;

    const body = { 
      name:uname1, 
      password:password1
    };
    

    const url = 'http://localhost:5000/api/signin'; 

    if (!this.uname) {
        this._snackBar.open('Username is empty', 'Close', {
          duration: 3000,
          verticalPosition: 'top',
          horizontalPosition: 'center'
        });
        setTimeout(() => {
          this.log_name_field.nativeElement.focus();
        }, 10);
    }
    else if(!this.password){
      this._snackBar.open('Password is empty', 'Close', {
        duration: 3000,
        verticalPosition: 'top',
        horizontalPosition: 'center'
      });
      setTimeout(() => {
        this.log_pass_field.nativeElement.focus();
      }, 10);
    }
    else{
      this.isLoading = true;
      this.authService.login(uname1, password1).subscribe(
        (response) => {
          if(response.statusCode==200){
            this.router.navigate(['/dashboard']);
            this.isLoading = false;
          }
          else{
            alert("Invalid Credentials !!!!")
            this.errorMessage = response.statusMessage;
            this.isLoading=false;
          }
        },
        (error) => {
          console.log(error);
        }
      );
      
      console.log(this.uname);
      console.log(this.password);
    }
  }

  onSignup(){

    if (!this.sp_uname) {
    //   alert('Please enter a value.');
      this._snackBar.open('Username is empty', 'Close', {
        duration: 3000,
        verticalPosition: 'top',
        horizontalPosition: 'center'
      });
      setTimeout(() => {
        this.sign_name_field.nativeElement.focus();
      }, 10);
    }
    else if(!this.sp_email){
      this._snackBar.open('Email is empty', 'Close', {
        duration: 3000,
        verticalPosition: 'top',
        horizontalPosition: 'center'
      });
      setTimeout(() => {
        this.sign_email_field.nativeElement.focus();
      }, 10);
    }

    else if(!this.sp_pass1){
      this._snackBar.open('Password is empty', 'Close', {
        duration: 3000,
        verticalPosition: 'top',
        horizontalPosition: 'center'
      });
      setTimeout(() => {
        this.sign_pass_field.nativeElement.focus();
      }, 10);
    }

    else if(!this.sp_pass2){
      this._snackBar.open('Please Re-Enter the Password', 'Close', {
        duration: 3000,
        verticalPosition: 'top',
        horizontalPosition: 'center'
      });
      setTimeout(() => {
        this.sign_pass_re_field.nativeElement.focus();
      }, 10);
    }

    else if(this.sp_pass1!=this.sp_pass2){
      this._snackBar.open('Password is not matching', 'Close', {
        duration: 3000,
        verticalPosition: 'top',
        horizontalPosition: 'center'
      });
      setTimeout(() => {
        this.sign_pass_re_field.nativeElement.focus();
      }, 10);
    }
  
    else{
      this.isLoading = true;
      const uname_signup=this.sp_uname;
      const password_signup=this.sp_pass1;
      const password_confirm_signup=this.sp_pass2;
      const email_signup=this.sp_email;

      const body_signup={
        name:this.sp_uname, 
        password:this.sp_pass1,
        email:this.sp_email
      }

      const url = 'http://localhost:5000/api/signup'; 
    
      this.authService.signup(this.sp_uname,this.sp_pass1,this.sp_email).subscribe(
        (Response)=>{
          if(Response.statusCode==200){
            this.router.navigate(['/dashboard']);
            this.isLoading = false;
          }
          else if(Response.statusMessage=="Username or email alread exists"){
            alert('Email or Username Already Exists Please try to login');
            this.isLoading=false;
          }
          else{
            this.errorMessage = Response.statusMessage;
          }
        },
        (error) => {
          console.log(error);
        }
      )

    }

  }

}
