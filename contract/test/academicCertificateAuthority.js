const AcademicCertificateAuthority = artifacts.require('AcademicCertificateAuthority');


async function assertThrows(promise, reason) {
  try {
    await promise;
  } catch (error) {
    assert.equal(error.reason, reason);
    return;
  }
  assert.fail('Should throw an error');
}

async function assertThrowsInView(promise, reason) {
  try {
    await promise;
  } catch (error) {
    assert.equal(Object.values(error.data)[0].reason, reason, reason);
    return;
  }
  assert.fail('Should throw an error');
}

contract('AcademicCertificateAuthority', () => {

  /*
    ADD REGULATOR
  */

  it('...should revert addRegulator() - not a supervisor', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    not_a_supervisor = (await web3.eth.getAccounts())[1];

    promise = contract.addRegulator(not_a_supervisor, 'Test Organization', 'Minsk', {'from': not_a_supervisor});
    await assertThrows(promise, 'Only supervisor is allowed to perform this operation');
  });

  it('...should revert addRegulator() - regulator address is empty', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    promise = contract.addRegulator('0x0000000000000000000000000000000000000000', 'Test Organization', 'Minsk');
    await assertThrows(promise, 'Regulator Address must not be empty');    
  });

  it('...should revert addRegulator() - issuer name is empty', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    not_a_supervisor = (await web3.eth.getAccounts())[1];

    promise = contract.addRegulator(not_a_supervisor, '', 'Minsk');
    await assertThrows(promise, 'Issuer Name must not be empty');
  });

  it('...should revert addRegulator() - issuer location is empty', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    not_a_supervisor = (await web3.eth.getAccounts())[1];

    promise = contract.addRegulator(not_a_supervisor, 'Test Organization', '');
    await assertThrows(promise, 'Issuer Location must not be empty');
  });

  it('...should add a regulator', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    accounts = await web3.eth.getAccounts();
    supervisor = accounts[0];
    regulator = accounts[1];

   	await contract.addRegulator(regulator, 'Test Organization', 'Minsk', {'from': supervisor});
  });


  /*
    ISSUE A CERTIFICATE AS REGULATOR OR SUPERVISOR
  */


  it('...should revert issueByRegulator() - not a regulator', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    not_a_regulator = (await web3.eth.getAccounts())[0];

    promise = contract.issueByRegulator('A123456', 'Ivan Ivanovich Ivanov', '123', 'diploma', 1620768986, 1620768986, 'Minsk, BY', 'Information Technology Software', {'from': not_a_regulator});
    await assertThrows(promise, 'Only regulator is allowed to perform this operation');
  });

  it('...should revert issueByRegulator() - certificate ID is empty', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    regulator = (await web3.eth.getAccounts())[1];

    promise = contract.issueByRegulator('', 'Ivan Ivanovich Ivanov', '123', 'diploma', 1620768986, 1620768986, 'Minsk, BY', 'Information Technology Software', {'from': regulator});
    await assertThrows(promise, 'Certificate ID must not be empty');
  });

  it('...should revert issueByRegulator() - student full name is empty', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    regulator = (await web3.eth.getAccounts())[1];

    promise = contract.issueByRegulator('A123456', '', '123', 'diploma', 1620768986, 1620768986, 'Minsk, BY', 'Information Technology Software', {'from': regulator});
    await assertThrows(promise, 'Student Full Name must not be empty');
  });

  it('...should revert issueByRegulator() - student guid is empty', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    regulator = (await web3.eth.getAccounts())[1];

    promise = contract.issueByRegulator('A123456', 'Ivan Ivanovich Ivanov', '', 'diploma', 1620768986, 1620768986, 'Minsk, BY', 'Information Technology Software', {'from': regulator});
    await assertThrows(promise, 'Student GUID must not be empty');
  });

  it('...should revert issueByRegulator() - certificate type is empty', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    regulator = (await web3.eth.getAccounts())[1];

    promise = contract.issueByRegulator('A123456', 'Ivan Ivanovich Ivanov', '123', '', 1620768986, 1620768986, 'Minsk, BY', 'Information Technology Software', {'from': regulator});
    await assertThrows(promise, 'Certificate Type must not be empty');
  });

  it('...should revert issueByRegulator() - certificate registration date is empty', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    regulator = (await web3.eth.getAccounts())[1];

    promise = contract.issueByRegulator('A123456', 'Ivan Ivanovich Ivanov', '123', 'diploma', 0, 1620768986, 'Minsk, BY', 'Information Technology Software', {'from': regulator});
    await assertThrows(promise, 'Certificate Release Date must not be empty');
  });

  it('...should revert issueByRegulator() - certificate release date is empty', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    regulator = (await web3.eth.getAccounts())[1];

    promise = contract.issueByRegulator('A123456', 'Ivan Ivanovich Ivanov', '123', 'diploma', 1620768986, 0, 'Minsk, BY', 'Information Technology Software', {'from': regulator});
    await assertThrows(promise, 'Certificate Release Date must not be empty');
  });

  it('...should revert issueByRegulator() - certificate place of issue is empty', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    regulator = (await web3.eth.getAccounts())[1];

    promise = contract.issueByRegulator('A123456', 'Ivan Ivanovich Ivanov', '123', 'diploma', 1620768986, 1620768986, '', 'Information Technology Software', {'from': regulator});
    await assertThrows(promise, 'Certificate Place of Issue must not be empty');
  });

  it('...should add a supervisor as a regulator', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    accounts = await web3.eth.getAccounts();
    supervisor = accounts[0];
    regulator = accounts[0];

    await contract.addRegulator(regulator, 'Supervisor Organization', 'Minsk', {'from': supervisor});
  });

  it('...should revert issueBySupervisor() - certificate organization is empty', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    supervisor = (await web3.eth.getAccounts())[0];

    promise = contract.issueBySupervisor('A123456', 'Ivan Ivanovich Ivanov', '123', 'diploma', 1620768986, 1620768986, '', 'Minsk, BY', 'Information Technology Software', {'from': supervisor});
    await assertThrows(promise, 'Certificate Organization must not be empty');
  });

  it('...should issue a certificate as regulator', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    regulator = (await web3.eth.getAccounts())[1];

	  result = await contract.issueByRegulator('A123456', 'Ivan Ivanovich Ivanov', '123', 'diploma', 1620768986, 1620768986, 'Minsk, BY', 'Information Technology Software', {'from': regulator});
	  assert.equal(result.logs[0].event, 'Issuance')
  });

  it('...should issue a certificate as supervisor', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    supervisor = (await web3.eth.getAccounts())[0];

    result = await contract.issueBySupervisor('A123457', 'Ivan Ivanovich Ivanov', '123', 'diploma', 1620768986, 1620768986, 'Smart Technologies LLC', 'Minsk, BY', 'Information Technology Software', {'from': supervisor});
    assert.equal(result.logs[0].event, 'Issuance')
  });

  it('...should revert issueByRegulator() - certificate already exists', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    regulator = (await web3.eth.getAccounts())[1];

    promise = contract.issueByRegulator('A123456', 'Petr Petrovich Petrov', '123', 'diploma', 1620768986, 1620768986, 'Minsk, BY', 'Information Technology Software', {'from': regulator});
    await assertThrows(promise, 'Certificate with a given ID already exists');
  });

  /*
    GET A CERTIFICATE BY ID
  */

  it('...should revert getCertificateById() - certificate id is empty', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    random_account = (await web3.eth.getAccounts())[3];

    promise = contract.getCertificateById('', {'from': random_account});
    await assertThrowsInView(promise, 'Certificate ID must not be empty');
  });

  it('...should revert getCertificateById() - certificate does not exist', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    random_account = (await web3.eth.getAccounts())[3];

    promise = contract.getCertificateById('XXXXXX', {'from': random_account});
    await assertThrowsInView(promise, 'Certificate with a given ID does not exist');
  });

  it('...should get certificate by its id', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    random_account = (await web3.eth.getAccounts())[3];

	  result = await contract.getCertificateById('A123456', {'from': random_account});
  });

  /*
    CANCEL A CERTIFICATE BY ID
  */


  it('...should revert cancel() - not a regulator', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    not_a_regulator = (await web3.eth.getAccounts())[3];

    promise = contract.cancel('A12345', {'from': not_a_regulator});
    await assertThrows(promise, 'Only regulator is allowed to perform this operation');
  });

  it('...should revert cancel() - certificate ID is empty', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    regulator = (await web3.eth.getAccounts())[1];

    promise = contract.cancel('', {'from': regulator});
    await assertThrows(promise, 'Certificate ID must not be empty');
  });

  it('...should revert cancel() - certificate does not exist', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    regulator = (await web3.eth.getAccounts())[1];

    promise = contract.cancel('XXXXXX', {'from': regulator});
    await assertThrows(promise, 'Certificate with a given ID does not exist');
  });

 it('...should cancel a certificate', async () => {
    const contract = await AcademicCertificateAuthority.deployed();

    accounts = await web3.eth.getAccounts();
    regulator = accounts[1];
    random_account = accounts[4];

	  result = await contract.cancel('A123456', {'from': regulator});
	  assert.equal(result.logs[0].event, 'Cancellation')

	  certificate = await contract.getCertificateById('A123456', {'from': random_account})
  });
});