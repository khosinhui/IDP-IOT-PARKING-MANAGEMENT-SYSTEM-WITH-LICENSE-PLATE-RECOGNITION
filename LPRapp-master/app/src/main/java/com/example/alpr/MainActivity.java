package com.example.alpr;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class MainActivity extends AppCompatActivity {

    EditText platenumber, topupbalance;
    TextView info;
    Button submit;
    DatabaseReference reff;
    User user;
    long maxid=0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        platenumber=(EditText) findViewById(R.id.etUserPlate);
        topupbalance=(EditText)findViewById(R.id.etUserBalance);
        info = (TextView)findViewById(R.id.tvUserInfo);
        submit = (Button)findViewById(R.id.btnUserEnter);
        user = new User();
        reff = FirebaseDatabase.getInstance().getReference().child("User");
        reff.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                if(dataSnapshot.exists()){
                    maxid=(dataSnapshot.getChildrenCount());
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });


        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                int balance = Integer.parseInt((topupbalance.getText().toString().trim()));
                user.setPlatenumber(platenumber.getText().toString().trim());
                user.setBalance(balance);
                reff.child(String.valueOf(maxid+1)).setValue(user);
                Toast.makeText(MainActivity.this,"Data inserted successfully",Toast.LENGTH_LONG).show();
            }
        });

    }
    }

