package Carsale;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JLabel;
import javax.swing.JOptionPane;

import java.awt.Font;
import javax.swing.SwingConstants;
import javax.swing.JTextField;
import javax.swing.RowFilter;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JTable;
import javax.swing.JScrollPane;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableRowSorter;

import net.proteanit.sql.DbUtils;

import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.awt.event.ActionEvent;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

public class Cardetails extends JFrame {
	
	Connection con=null;
	PreparedStatement pst=null;
	ResultSet rs=null;
	
	String url= "jdbc:mysql://localhost/carsale";
	String uname = "root";
	String pass = "";

	private JPanel contentPane;
	private JTextField txtModel;
	private JTextField txtManu;
	private JTextField txtYear;
	private JTextField txtMileage;
	private JTextField txtPrice;
	private JTable table;

	
	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Cardetails frame = new Cardetails();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	public Cardetails() {
		setTitle("Car Details");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 995, 687);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel lblCardet = new JLabel("Car Details");
		lblCardet.setForeground(new Color(160, 82, 45));
		lblCardet.setHorizontalAlignment(SwingConstants.CENTER);
		lblCardet.setFont(new Font("Lucida Bright", Font.BOLD, 22));
		lblCardet.setBounds(310, 22, 560, 42);
		contentPane.add(lblCardet);
		
		JLabel lblModel = new JLabel("Model");
		lblModel.setHorizontalAlignment(SwingConstants.CENTER);
		lblModel.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lblModel.setBounds(29, 67, 126, 33);
		contentPane.add(lblModel);
		
		txtModel = new JTextField();
		txtModel.setBounds(29, 98, 126, 33);
		contentPane.add(txtModel);
		txtModel.setColumns(10);
		
		JLabel lblManufacturer = new JLabel("Manufacturer");
		lblManufacturer.setHorizontalAlignment(SwingConstants.CENTER);
		lblManufacturer.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lblManufacturer.setBounds(29, 144, 126, 33);
		contentPane.add(lblManufacturer);
		
		txtManu = new JTextField();
		txtManu.setColumns(10);
		txtManu.setBounds(29, 175, 126, 33);
		contentPane.add(txtManu);
		
		JLabel lblYear = new JLabel("Year");
		lblYear.setHorizontalAlignment(SwingConstants.CENTER);
		lblYear.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lblYear.setBounds(29, 223, 126, 33);
		contentPane.add(lblYear);
		
		txtYear = new JTextField();
		txtYear.addKeyListener(new KeyAdapter() {
			@Override
			public void keyTyped(KeyEvent e) {
				char y = e.getKeyChar();
				if (Character.isLetter(y)) {
					txtYear.setEditable(false);
					JOptionPane.showMessageDialog(null,"Enter a valid year");
				}
				else {
					txtYear.setEditable(true);
				}
			}
		});
		txtYear.setColumns(10);
		txtYear.setBounds(29, 248, 126, 33);
		contentPane.add(txtYear);
		
		JLabel lblMileage = new JLabel("Mileage");
		lblMileage.setHorizontalAlignment(SwingConstants.CENTER);
		lblMileage.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lblMileage.setBounds(29, 308, 126, 33);
		contentPane.add(lblMileage);
		
		txtMileage = new JTextField();
		txtMileage.setColumns(10);
		txtMileage.setBounds(29, 335, 126, 33);
		contentPane.add(txtMileage);
		
		JLabel lblPrice = new JLabel("Price");
		lblPrice.setHorizontalAlignment(SwingConstants.CENTER);
		lblPrice.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lblPrice.setBounds(29, 388, 126, 33);
		contentPane.add(lblPrice);
		
		txtPrice = new JTextField();
		txtPrice.addKeyListener(new KeyAdapter() {
			@Override
			public void keyTyped(KeyEvent e) {
				char p = e.getKeyChar();
				if (Character.isLetter(p)) {
					txtPrice.setEditable(false);
					JOptionPane.showMessageDialog(null,"Enter a valid amount");
				}
				else {
					txtPrice.setEditable(true);
				}
			}
		});
		txtPrice.setColumns(10);
		txtPrice.setBounds(29, 413, 126, 33);
		contentPane.add(txtPrice);
		
		JButton btnAdd = new JButton("Add");
		btnAdd.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					
					String query = "INSERT INTO `cardetails`(`Model`, `Manufacturer`, `Year`, `Mileage`, `Price`) VALUES (?,?,?,?,?)";
					connection();
					pst =con.prepareStatement(query);
					
					if(txtModel.getText().length()!=0) {
					pst.setString(1,txtModel.getText());
					}else
						JOptionPane.showMessageDialog(null,"Enter Model");
					
					if(txtManu.getText().length()!=0) {	
					pst.setString(2,txtManu.getText());
					}else
						JOptionPane.showMessageDialog(null,"Enter Manufacturer");
					
					if(txtYear.getText().length()!=0) {
					pst.setString(3,txtYear.getText());
					}else
						JOptionPane.showMessageDialog(null,"Enter Year");
					
					if(txtMileage.getText().length()!=0) {
					pst.setString(4,txtMileage.getText());
					}else
						JOptionPane.showMessageDialog(null,"Enter Milaeage");
					
					if(txtPrice.getText().length()!=0) {
					pst.setString(5,txtPrice.getText());
					}else
						JOptionPane.showMessageDialog(null,"Enter Price");
					
					pst.executeUpdate();
					
					txtModel.setText("");
					txtManu.setText("");
					txtYear.setText("");
					txtMileage.setText("");
					txtPrice.setText("");
					
		            JOptionPane.showMessageDialog(null,"Car Added Successfully");
		            }catch(Exception ex) {
//		            	JOptionPane.showMessageDialog(null,"Error Occured!"+ex);
		            }
				}
			
		});
		btnAdd.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnAdd.setBounds(30, 469, 125, 33);
		contentPane.add(btnAdd);
		
		JButton btnUpdate = new JButton("Update");
		btnUpdate.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				
				try {
					//Data validation
					if(txtModel.getText().length()!=0) {
						Statement stmt =  con.createStatement();
						//Wants to check whether the relevant entry exist
						String car = txtModel.getText();
						String qryExist = "SELECT * FROM `cardetails` WHERE Model='"+ car +"'";
						rs=stmt.executeQuery(qryExist);
						
							if (rs.next()) {
								if (txtManu.getText().length() != 0) {
									String query1 = "UPDATE `cardetails` SET `Manufacturer`=? WHERE Model=?";
									connection();
									pst = con.prepareStatement(query1);
									pst.setString(1, txtManu.getText());
									pst.setString(2, txtModel.getText());
									pst.executeUpdate();
									txtManu.setText("");
									JOptionPane.showMessageDialog(null, "Manufacturer Updated");
									refresh();
								}
								if (txtYear.getText().length() != 0) {
									String query2 = "UPDATE `cardetails` SET `Year`=? WHERE Model=?";
									connection();
									pst = con.prepareStatement(query2);
									pst.setString(2, txtModel.getText());
									pst.setString(1, txtYear.getText());
									pst.executeUpdate();
									txtYear.setText("");
									JOptionPane.showMessageDialog(null, "Year Updated");
									refresh();
								}
								if (txtMileage.getText().length() != 0) {
									String query3 = "UPDATE `cardetails` SET `Mileage`=? WHERE Model=?";
									connection();
									pst = con.prepareStatement(query3);
									pst.setString(2, txtModel.getText());
									pst.setString(1, txtMileage.getText());
									pst.executeUpdate();
									txtMileage.setText("");
									JOptionPane.showMessageDialog(null, "Mileage Updated");
									refresh();
								}
								if (txtPrice.getText().length() != 0) {
									String query4 = "UPDATE `cardetails` SET `Price`=? WHERE Model=?";
									connection();
									pst = con.prepareStatement(query4);
									pst.setString(2, txtModel.getText());
									pst.setString(1, txtPrice.getText());
									pst.executeUpdate();
									txtPrice.setText("");
									JOptionPane.showMessageDialog(null, "Price Updated");
									refresh();
								} 
							}else
								JOptionPane.showMessageDialog(null,"Car Model does not exist");
							txtModel.setText("");
					}else
						JOptionPane.showMessageDialog(null,"Enter Model to Update");
					
				   
		            }catch(Exception ex) {
		            	JOptionPane.showMessageDialog(null,"Error Occured!"+ex);
		            
		            }
				
			}
		});
		btnUpdate.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnUpdate.setBounds(29, 512, 126, 33);
		contentPane.add(btnUpdate);
		
		JButton btnDel = new JButton("Delete");
		btnDel.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				
				try {

					connection();
					Statement stmt =  con.createStatement();
					
					if(txtModel.getText().length()!=0) {
						//Wants to check whether the relevant entry exist
						String carModel = txtModel.getText();
						String qryExist = "SELECT * FROM `cardetails` WHERE Model='"+ carModel+"'";
						rs=stmt.executeQuery(qryExist);
						
						if(rs.next()) { 
							// if the entry exists, will delete it
							String query = "DELETE FROM `cardetails` WHERE Model=?";
							pst =con.prepareStatement(query);
							pst.setString(1,txtModel.getText());
							pst.executeUpdate();
							JOptionPane.showMessageDialog(null,"Successfully deleted");
							refresh();
							txtModel.setText("");
						}
						else {
							JOptionPane.showMessageDialog(null,"Car Model does not exist");
							txtModel.setText("");
						}
					}else 
						JOptionPane.showMessageDialog(null,"Enter the Model to delete");
										
						            
		            }catch(Exception ex) {
		            	JOptionPane.showMessageDialog(null,"error : "+ex);
		            }
				
			}
		});
		btnDel.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnDel.setBounds(29, 555, 126, 33);
		contentPane.add(btnDel);
		
		JButton btnBack = new JButton("Back");
		btnBack.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				Admin newWindow2 = new Admin();
	            newWindow2.setVisible(true);
	            setVisible(false);
			}
		});
		btnBack.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnBack.setBounds(30, 598, 125, 33);
		contentPane.add(btnBack);
		
		JScrollPane scrollPane = new JScrollPane();
		scrollPane.setBounds(206, 98, 765, 498);
		contentPane.add(scrollPane);
		
		table = new JTable();
		scrollPane.setViewportView(table);
		table.setModel(new DefaultTableModel(
			new Object[][] {
			},
			new String[] {
				"Model", "Manufacturer", "Year", "Mileage", "Price"
			}
		));
		
		JButton btnRefresh = new JButton("Refresh Details");
		btnRefresh.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				refresh();
				
			}
		});
		btnRefresh.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnRefresh.setBounds(788, 606, 183, 41);
		contentPane.add(btnRefresh);
		
		JLabel lblNewLabel = new JLabel("");
		ImageIcon img2 = new ImageIcon(this.getClass().getResource("/resources/img11.png"));
		lblNewLabel.setIcon(img2);
		lblNewLabel.setBounds(252, 10, 231, 90);
		contentPane.add(lblNewLabel);
	}
	
	public void refresh() {
		try {
			
			connection();
			String query = "SELECT * FROM `cardetails`";
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