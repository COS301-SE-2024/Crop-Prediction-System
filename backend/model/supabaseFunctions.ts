import { SupabaseClient } from "@supabase/supabase-js";
let supabase = new SupabaseClient("https://iimtpbzfrdcuuklwnprq.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlpbXRwYnpmcmRjdXVrbHducHJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTU4MTQ1MDMsImV4cCI6MjAzMTM5MDUwM30.o2gbIkgZaTQlFRLabs-abzkim462xatVumMJXo06m6w")

// signUp new user
export async function signUp(email: string, password: string) {
    let { data, error } = await supabase.auth.signUp({
        email: email,
        password: password,
    });
    if(data && !error && data.user) {
    // add to users table in database
    supabase.from('users').insert([
      { email: email, id: data.user.id },
    ]);
    }
}

// login user
export async function login(email: string, password: string){
    let {  data, error } = await supabase.auth.signInWithPassword({
        email: email,
        password: password,
    });
    if(data && !error) {
        return {
            success: true
        }
    }else{
        return {
            success: false,
            error: error
        }
    }
}

// get user
export async function getUser(){
    let {data, error} = await supabase.auth.getUser();
    if(data && !error){
        return {data:data}
    }else{
        return {error:error}
    }
}

// logout user
export async function logout(){
    let {error} = await supabase.auth.signOut();
    if(!error){
        return {success:true}
    }else{
        return {success:false, error:error}
    }
}