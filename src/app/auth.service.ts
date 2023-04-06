import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

@Injectable({
    providedIn: 'root'
  })
  export class AuthService {
    getToken() {
        throw new Error('Method not implemented.');
    }

    private loggedIn = false;
  
    constructor(private http: HttpClient) { }
  
    // Methods for authentication will go here

    login(username: string, password: string): Observable<any> {
        return this.http.post<any>('http://localhost:5000/api/signin', { name: username, password: password })
        .pipe(
            tap(() => this.loggedIn = true)
          );
      }


      signup(username:string,password:string,email:string):Observable<any>{
        return this.http.post<any>('http://localhost:5000/api/signup',{name:username,email:email,password:password})
      }

    isLoggedIn() {
        return this.loggedIn;
    }
  }