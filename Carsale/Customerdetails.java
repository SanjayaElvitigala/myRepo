package Carsale;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.EventQueue;
import net.proteanit.sql.DbUtils;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;
import javax.swing.JScrollPane;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import java.awt.Font;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.awt.event.ActionEvent;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

public class Customerdetails extends JFrame {
	
	Connection con=null;
	PreparedStatement pst=null;
	ResultSet rs=null;
	
	String url= "jdbc:mysql://localhost/carsale";
	String uname = "root";
	String pass = "";

	private JPanel contentPane;
	private JTable table;
	private JTextField txtCustID;
	private JTextField txtCustName;
	private JTextField txtCustAddress;
	private JTextField txtCustTel;
	private JTextField txtDate;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Customerdetails frame = new Customerdetails();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 */
	public Customerdetails() {
		setTitle("Customer Details");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 995, 687);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JScrollPane scrollPane = new JScrollPane();
		scrollPane.setBounds(209, 58, 749, 517);
		contentPane.add(scrollPane);
		
		table = new JTable();
		scrollPane.setViewportView(table);
		table.setModel(new DefaultTableModel(
			new Object[][] {
			},
			new String[] {
				"Id", "Name", "Address", "Contact", "Date"
			}
		));
		
		JButton btnFetch = new JButton("Refresh Details");
		btnFetch.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				refresh();
			}
		});
		btnFetch.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnFetch.setBounds(787, 585, 171, 42);
		contentPane.add(btnFetch);
		
		JLabel lbID = new JLabel("ID");
		lbID.setHorizontalAlignment(SwingConstants.CENTER);
		lbID.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lbID.setBounds(30, 124, 126, 13);
		contentPane.add(lbID);
		
		txtCustID = new JTextField();
		txtCustID.setBounds(30, 140, 126, 33);
		contentPane.add(txtCustID);
		txtCustID.setColumns(10);
		
		JLabel lblName = new JLabel("Name");
		lblName.setHorizontalAlignment(SwingConstants.CENTER);
		lblName.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lblName.setBounds(30, 183, 126, 13);
		contentPane.add(lblName);
		
		txtCustName = new JTextField();
		txtCustName.setColumns(10);
		txtCustName.setBounds(30, 198, 126, 33);
		contentPane.add(txtCustName);
		
		JLabel lbIAddress = new JLabel("Address");
		lbIAddress.setHorizontalAlignment(SwingConstants.CENTER);
		lbIAddress.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lbIAddress.setBounds(30, 250, 126, 13);
		contentPane.add(lbIAddress);
		
		txtCustAddress = new JTextField();
		txtCustAddress.setColumns(10);
		txtCustAddress.setBounds(30, 262, 126, 33);
		contentPane.add(txtCustAddress);
		
		JLabel lbITel = new JLabel("Telephone");
		lbITel.setHorizontalAlignment(SwingConstants.CENTER);
		lbITel.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lbITel.setBounds(30, 305, 126, 24);
		contentPane.add(lbITel);
		
		txtCustTel = new JTextField();
		txtCustTel.addKeyListener(new KeyAdapter() {
			@Override
			public void keyTyped(KeyEvent e) {
				char y = e.getKeyChar();
				if (Character.isLetter(y)) {
					txtCustTel.setEditable(false);
					JOptionPane.showMessageDialog(null,"Enter a valid year");
				}
				else {
					txtCustTel.setEditable(true);
				}
			}
		});
		txtCustTel.setColumns(10);
		txtCustTel.setBounds(30, 325, 126, 33);
		contentPane.add(txtCustTel);
		
		JButton btnUpdate = new JButton("Update");
		btnUpdate.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				
				try {
					String query = "UPDATE `customerreg` SET `Name`=?,`Address`=?,`Contact`=? WHERE Id=?";
					connection();
					pst =con.prepareStatement(query);
					
					//Data validation
					
					if(txtCustID.getText().length()!=0) {
						Statement stmt =  con.createStatement();
						//Wants to check whether the relevant entry exist
						String customer = txtCustID.getText();
						String qryExist = "SELECT * FROM `customerreg` WHERE Id='"+ customer +"'";
						rs=stmt.executeQuery(qryExist);
						
						if (rs.next()) {
							if (txtCustName.getText().length() != 0) {
								String queryName = "UPDATE `customerreg` SET `Name`=? WHERE Id=?";
								connection();
								pst = con.prepareStatement(queryName);
								pst.setString(1, txtCustName.getText());
								pst.setString(2, txtCustID.getText());
								pst.executeUpdate();
								txtCustName.setText("");
								JOptionPane.showMessageDialog(null, "Name Updated");
							}
							if (txtCustAddress.getText().length() != 0) {
								String queryAddress = "UPDATE `customerreg` SET `Address`=? WHERE Id=?";
								connection();
								pst = con.prepareStatement(queryAddress);
								pst.setString(2, txtCustID.getText());
								pst.setString(1, txtCustAddress.getText());
								pst.executeUpdate();
								txtCustAddress.setText("");
								JOptionPane.showMessageDialog(null, "Address Updated");
							}
							if (txtCustTel.getText().length() != 0) {
								String queryTel = "UPDATE `customerreg` SET `Contact`=? WHERE Id=?";
								connection();
								pst = con.prepareStatement(queryTel);
								pst.setString(2, txtCustID.getText());
								pst.setString(1, txtCustTel.getText());
								pst.executeUpdate();
								txtCustTel.setText("");
								JOptionPane.showMessageDialog(null, "Contact Number Updated");
							}
							refresh();
						}else
							JOptionPane.showMessageDialog(null,"The Customer does not exist");
					}else
						JOptionPane.showMessageDialog(null,"Enter ID to Update");
					
				   
					}catch(Exception ex) {
		            	JOptionPane.showMessageDialog(null,"Error Occured!"+ex);
		            }
				
			}
		});
		btnUpdate.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnUpdate.setBounds(30, 426, 126, 33);
		contentPane.add(btnUpdate);
		
		JButton btnDelete = new JButton("Delete");
		btnDelete.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				
				try {

					connection();
					Statement stmt =  con.createStatement();
					
					if(txtCustID.getText().length()!=0) {
						//Wants to check whether the relevant entry exist
						String customer = txtCustID.getText();
						String qryExist = "SELECT * FROM `customerreg` WHERE Id='"+ customer +"'";
						rs=stmt.executeQuery(qryExist);
						
						if(rs.next()) { 
							// if the entry exists, will delete it
							String query = "DELETE FROM `customerreg` WHERE Id=?";
							pst =con.prepareStatement(query);
							pst.setString(1,txtCustID.getText());
							pst.executeUpdate();
							JOptionPane.showMessageDialog(null,"Successfully deleted");
							refresh();
						}
						else
							JOptionPane.showMessageDialog(null,"Customer does not exist");
							
						
					}else 
						JOptionPane.showMessageDialog(null,"Enter the Customer ID to delete");
										
						            
		            }catch(Exception ex) {
		            	JOptionPane.showMessageDialog(null,"error : "+ex);
		            }
			}
		});
		btnDelete.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnDelete.setBounds(30, 469, 126, 33);
		contentPane.add(btnDelete);
		
		JButton btnBack = new JButton("Back");
		btnBack.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				Admin newWindow2 = new Admin();
	            newWindow2.setVisible(true);
	            setVisible(false);
				
			}
		});
		btnBack.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnBack.setBounds(30, 511, 126, 33);
		contentPane.add(btnBack);
		
		JLabel lblCustomerDetails = new JLabel("Customer Details");
		lblCustomerDetails.setForeground(new Color(160, 82, 45));
		lblCustomerDetails.setHorizontalAlignment(SwingConstants.CENTER);
		lblCustomerDetails.setFont(new Font("Lucida Bright", Font.BOLD, 22));
		lblCustomerDetails.setBounds(209, 10, 749, 42);
		contentPane.add(lblCustomerDetails);
		ImageIcon img1 = new ImageIcon(this.getClass().getResource("/resources/img6.png"));
		
		JButton btnAdd = new JButton("Add");
		btnAdd.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					
					String query = "INSERT INTO `customerreg`(`Id`, `Name`, `Address`, `Contact`, `Date`) VALUES (?,?,?,?,?)";
					connection();
					pst =con.prepareStatement(query);
					
					if(txtDate.getText().length()!=0) {
						pst.setString(5,txtDate.getText());
					}else
						JOptionPane.showMessageDialog(null,"Enter Contact Date");
					if(txtCustID.getText().length()!=0) {
					pst.setString(1,txtCustID.getText());
					}else
						JOptionPane.showMessageDialog(null,"Enter ID");
					
					if(txtCustName.getText().length()!=0) {	
					pst.setString(2,txtCustName.getText());
					}else
						JOptionPane.showMessageDialog(null,"Enter Name");
					
					if(txtCustAddress.getText().length()!=0) {
					pst.setString(3,txtCustAddress.getText());
					}else
						JOptionPane.showMessageDialog(null,"Enter Address");
					
					if(txtCustTel.getText().length()!=0) {
					pst.setString(4,txtCustTel.getText());
					}else
						JOptionPane.showMessageDialog(null,"Enter Contact Number");
					
					
					
					pst.executeUpdate();
					
					txtCustID.setText("");
					txtCustName.setText("");
					txtCustAddress.setText("");
					txtCustTel.setText("");
				
					
		            JOptionPane.showMessageDialog(null,"Customer Added Successfully");
		            refresh();
		            }catch(Exception ex) {
//		            	JOptionPane.showMessageDialog(null,"Error Occured!"+ex);
		            }
			}
		});
		btnAdd.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnAdd.setBounds(30, 383, 126, 33);
		contentPane.add(btnAdd);
		
		txtDate = new JTextField();
		txtDate.setColumns(10);
		txtDate.setBounds(30, 81, 126, 33);
		contentPane.add(txtDate);
		
		JLabel lbIdate = new JLabel("Date");
		lbIdate.setHorizontalAlignment(SwingConstants.CENTER);
		lbIdate.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lbIdate.setBounds(30, 58, 126, 13);
		contentPane.add(lbIdate);
	}
	
	public void refresh() {
		try {
			
			connection();
			String query = "SELECT * FROM `customerreg`";
			pst =con.prepareStatement(query);
			rs=pst.executeQuery();
			
			table.setModel(DbUtils.resultSetToTableModel(rs));
			
			
		
		}catch(Exception ex) {
			System.out.println(ex);
		}
	}
	
	public void connection() {
		try {
			Class.forName("com.mysql.cj.jdbc.Driver");
			con =DriverManager.getConnection(url, uname, pass);
			
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
}

