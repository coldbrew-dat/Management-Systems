#include <iostream>
#include <fstream>
#include <string>
using namespace std;

// HOTEL CLASS
class Hotel {
private:
    string hotel_name;
    int total_rooms;
    int total_guests;

public:
    Hotel() : hotel_name(""), total_rooms(0), total_guests(0) {}
    Hotel(string name, int rooms, int guests) : hotel_name(name), total_rooms(rooms), total_guests(guests) {}

    void setHotelName(string n) { hotel_name = n; }
    void setTotalRooms(int r) { total_rooms = r; }
    void setTotalGuests(int g) { total_guests = g; }

    string getHotelName() const { return hotel_name; }
    int getTotalRooms() const { return total_rooms; }
    int getTotalGuests() const { return total_guests; }

    virtual void display() const = 0;
    virtual void manager() { cout << "Base Hotel Manager Function\n"; }

    virtual ~Hotel() { }
};

// ROOM  CLASS
class Room {
protected:
    int room_no;
    string room_type;
public:
    static int count; // declaration only

    Room() : room_no(0), room_type("standard") { count++; }
    Room(int no, string type) : room_no(no), room_type(type) { count++; }

    void setRoomNo(int n) { room_no = n; }
    void setRoomType(string t) { room_type = t; }

    int getRoomNo() const { return room_no; }
    string getRoomType() const { return room_type; }

    virtual void display() const { }
    virtual ~Room() {}
};

// Static member definition
int Room::count = 0;


// Derived Rooms / INHERITANCE
class StandardRoom : public Room {
public:
    StandardRoom(int no) : Room(no, "standard") {}
    void display() const  { }
};

class DeluxeRoom : public Room {
public:
    DeluxeRoom(int no) : Room(no, "deluxe") {}
    void display() const  { }
};

class SuiteRoom : public Room {
public:
    SuiteRoom(int no) : Room(no, "suite") {}
    void display() const  { }
};

// PAYMENT
class PaymentStatus;

class Payment {
private:
    string date;
    bool status;
    Room* room; //AGGREGATION

public:
    Payment() : date(""), status(false), room(NULL) {}
    Payment(string d, Room* r, bool s) : date(d), room(r), status(s) {}

    void setDate(string d) { date = d; }
    void setStatus(bool s) { status = s; }

    float calculateCharges() const {
        if(!room) return 0;
        if(room->getRoomType() == "standard") return 500;
        if(room->getRoomType() == "deluxe") return 1500;
        if(room->getRoomType() == "suite") return 3000;
        return 0;
    }
    
    //Operator Overloading
    float operator-(float discount) const { return calculateCharges() - discount; }
    float operator+(float extra) const { return calculateCharges() + extra; }

    void process() { if(!status) throw string("Payment failed!"); }

    friend void verifyPayment(Payment &p);
    friend class PaymentStatus;

    ~Payment() {}
};

void verifyPayment(Payment &p) {}

// GUEST CLASS
class Guest {
private:
    const string guestID;
    string name;
    bool payment_status;
    bool cnic_verified;
    static int count;
    Payment* payment;

public:
    Guest() : guestID("G000"), name(""), payment_status(false), cnic_verified(false), payment(NULL) { count++; }
    Guest(string id, string n, bool pay, bool cnic) : guestID(id), name(n), payment_status(pay), cnic_verified(cnic), payment(NULL) { count++; }

    Guest(const Guest &g) : guestID(g.guestID), name(g.name), payment_status(g.payment_status), cnic_verified(g.cnic_verified), payment(g.payment) { count++; } // shallow
    Guest(const Guest &g, bool deep) : guestID(g.guestID), name(g.name), payment_status(g.payment_status), cnic_verified(g.cnic_verified) {
        if(deep && g.payment) payment = new Payment(*g.payment); else payment = g.payment;
        count++;
    }

    void assignPayment(Payment* p) { payment = p; }

    void saveToFile() {
    ofstream file("guests.txt", ios::app);
    file << "Guest ID: " << guestID
         << " | Name: " << name
         << " | Payment Status: " << (payment_status ? "Paid" : "Unpaid")
         << " | CNIC Verified: " << (cnic_verified ? "Yes" : "No")
         << endl;
    file.close();
}


    static int getGuestCount() { return count; }

    ~Guest() { if(payment) delete payment; }
};
int Guest::count = 0;

//MANAGER =
class Manager {
protected:
    string name;
    string role;
    static int count;

public:
    Manager() : name("None"), role("None") {}
    Manager(string n, string r) : name(n), role(r) { count++; }

    virtual void manager() { }
    string getName() const { return name; }

    void saveToFile() {
    ofstream file("managers.txt", ios::app);
    file << "Manager Name: " << name
         << " | Position: " << role
         << endl;
    file.close();
}
    static int getManagerCount() { return count; }

    virtual ~Manager() {}
};
int Manager::count = 0;

class LobbyManager : public Manager {
public:
    LobbyManager(string n) : Manager(n, "Lobby") {}
    void manager()  {}
};

class OperationsManager : public Manager {
public:
    OperationsManager(string n) : Manager(n, "Operations") {}
    void manager()  {}
};

//RESERVATION
class Reservation {
private:
    string guestName;
    int room_no;
    string room_type;
    bool payment_done;

public:
    Reservation() : guestName(""), room_no(0), room_type(""), payment_done(false) {}
    Reservation(string g, int rno, string type, bool pay) : guestName(g), room_no(rno), room_type(type), payment_done(pay) {}

    void saveToFile() {
    ofstream file("reservations.txt", ios::app);
    file << "Guest Name: " << guestName
         << " | Room No: " << room_no
         << " | Room Type: " << room_type
         << " | Payment Done: " << (payment_done ? "Yes" : "No")
         << endl;
    file.close();
}

};

int main() {
    int choice;
    do {
        cout << "\nMAIN MENU\n";
        cout << "1. Make Reservation\n";
        cout << "2. Manager Section\n";
        cout << "3. Show Totals\n";
        cout << "4. Exit\n";
        cout << "Enter choice: ";
        cin >> choice;

        if(choice == 1) {
            string guestID, guestName, roomType, paymentInput;
            int roomNo;
            bool paymentDone = false;

            cout << "--- MAKE RESERVATION ---\n";
            cout << "Enter Guest ID: "; cin >> guestID;
            cout << "Enter Guest Name: "; cin >> guestName;
            cout << "Enter Room No: "; cin >> roomNo;
            cout << "Enter Room Type (standard/deluxe/suite): "; cin >> roomType;
            cout << "Payment Done? (Yes/No): "; cin >> paymentInput;

            if (paymentInput == "Yes" || paymentInput == "yes" || paymentInput == "1")
                paymentDone = true;

            Room* r;
            if(roomType == "standard") r = new StandardRoom(roomNo);
            else if(roomType == "deluxe") r = new DeluxeRoom(roomNo);
            else r = new SuiteRoom(roomNo);

            Payment* p = new Payment("2025-12-07", r, paymentDone);

            Guest g(guestID, guestName, paymentDone, true);
            g.assignPayment(p);

            Reservation res(guestName, roomNo, roomType, paymentDone);

            try {
                // Save files
                ofstream guestFile("guests.txt", ios::app);
                guestFile << "Guest ID: " << guestID 
                          << " | Name: " << guestName 
                          << " | Payment Status: " << (paymentDone ? "Paid" : "Pending") 
                          << " | CNIC Verified: Yes" << endl;
                guestFile.close();

                ofstream resFile("reservations.txt", ios::app);
                resFile << "Guest Name: " << guestName
                        << " | Room No: " << roomNo
                        << " | Room Type: " << roomType
                        << " | Payment Status: " << (paymentDone ? "Paid" : "Pending") << endl;
                resFile.close();

                ofstream payFile("payments.txt", ios::app);
                payFile << "Payment Date: " << "2025-12-07"
                        << " | Room Type: " << roomType
                        << " | Status: " << (paymentDone ? "Paid" : "Pending") << endl;
                payFile.close();

                cout << "Reservation Successful!\n";
                if(paymentDone)
                    cout << "Payment Successful!\n";
                else
                    cout << "Payment Pending!\n";

            } catch(...) {
                cout << "Error saving data!\n";
            }

            delete r;
            delete p;

        } else if(choice == 2) {
            int mChoice;
            cout << "--- MANAGER SECTION ---\n";
            cout << "1. Add Manager\n2. Show Managers\nEnter choice: ";
            cin >> mChoice;

            if(mChoice == 1) {
                string mName, role;
                cout << "Enter Manager Name: "; cin >> mName;
                cout << "Enter Role (Lobby/Operations): "; cin >> role;
                Manager* m;

                if(role == "Lobby") m = new LobbyManager(mName);
                else if(role == "Operations") m = new OperationsManager(mName);
                else { cout << "Invalid Role!\n"; continue; }

                ofstream file("managers.txt", ios::app);
                file << "Manager Name: " << m->getName() 
                     << " | Position: " << role << endl;
                file.close();

                cout << "Manager Added!\n";
                delete m;

            } else if(mChoice == 2) {
                ifstream file("managers.txt");
                string line;
                cout << "--- MANAGERS LIST ---\n";
                while(getline(file,line)) cout << line << endl;
                file.close();
            } else {
                cout << "Invalid choice!\n";
            }

        } else if(choice == 3) {
        	
    // Count guests from file
    ifstream guestFile("guests.txt");
    int guestCount = 0; string line;
    while(getline(guestFile,line)) guestCount++;
    guestFile.close();

    // Count managers from file
    ifstream mFile("managers.txt");
    int mCount = 0;
    while(getline(mFile,line)) mCount++;
    mFile.close();

    cout << "Total Guests: " << guestCount << endl;
    cout << "Total Managers: " << mCount << endl;
}


    } while(choice != 4);

    return 0;
}

