var AcademicCertificateAuthority = artifacts.require("AcademicCertificateAuthority");

module.exports = function(deployer) {
  deployer.deploy(AcademicCertificateAuthority);
};
